// trading_engine module
//
// Left some comments here and there. Am confident that this is either already
// or very close to synthesizable. Trade execution is down to 1-cycle latency
// after final TCP data (buy/sell bit).
//
// Author: Gunvir Ranu
// Email:  mail@gunvirranu.com

module trading_engine (
    input  logic        clk,                // Clock
    input  logic        rst,                // Active high asynchronous reset

    input  logic [15:0] product_num,        // Product number
    input  logic [31:0] product_theo,       // Theo for product
    input  logic        product_theo_valid, // Product and theo valid

    input  logic [7:0]  tcp_data,           // TCP data stream
    input  logic        tcp_valid,          // TCP valid data
    input  logic        tcp_sop,            // TCP start of packet
    input  logic        tcp_eop,            // TCP end of packet

    input  logic [31:0] px_offset,          // Price offset
    input  logic        px_offset_valid,    // Price offset valid

    output logic        trade               // Execute trade
);

    // Max length of the TCP packet needed for data.
    // Okay if packet continues longer, but cannot count/index further.
    localparam integer MAX_TCP_INDEX    = 40;
    localparam integer I_TCP            = ($clog2(MAX_TCP_INDEX + 1) - 1);
    // Indices of data bytes in TCP packet stream
    localparam logic[I_TCP:0] I_PRODUCT_MSB = 'd30;
    localparam logic[I_TCP:0] I_PRODUCT_LSB = 'd31;
    localparam logic[I_TCP:0] I_PRICE_MSB   = 'd34;
    localparam logic[I_TCP:0] I_PRICE_LSB   = 'd37;
    localparam logic[I_TCP:0] I_BUY_NSELL   = 'd40;

    typedef logic[15:0] product_t;
    typedef logic[31:0] price_t;
    typedef enum logic [2:0] {
        RESET,
        IDLE,
        WAIT_FOR_PACKET_PRODUCT,
        WAIT_FOR_PACKET_PRICE,
        WAIT_FOR_PACKET_BUY,
        OUTPUT_TRADE,
        WAIT_FOR_PACKET_END
    } state_t;

    // Module I/O
    product_t       product_num_rw;
    price_t         px_offset_latched;
    price_t         theo_saved;
    // TCP
    product_t       product_tcp;
    price_t         price_tcp;
    logic           buy_nsell_tcp;
    logic [I_TCP:0] packet_index;
    // Internal
    state_t         state = RESET;
    price_t         trade_price;
    logic           should_trade;
    logic           trade_req;

    product_theo_table #(
        .PROD_BITS  ( 16 ),
        .THEO_BITS  ( 32 )
    ) product_theo_table_inst (
        .clk        ( clk                   ),
        .srst       ( 1'b0                  ),  // See comment in `product_theo_table`
        .save_theo  ( product_theo_valid    ),
        .product    ( product_num_rw        ),
        .theo_in    ( product_theo          ),
        .theo_out   ( theo_saved            )
    );

    assign product_num_rw = (product_theo_valid ? product_num : product_tcp);
    assign trade = (trade_req && (~rst));

    // Value of `should_trade` only to be consumed when all inputs are valid
    always_comb begin
        if (buy_nsell_tcp) begin
            // Market is buying what we're selling
            trade_price = (theo_saved + px_offset_latched);
            should_trade = (price_tcp >= trade_price);
        end else begin
            // We're buying what the market is selling
            trade_price = (theo_saved - px_offset_latched);
            should_trade = (price_tcp <= trade_price);
        end
    end

    always_ff @(posedge clk, posedge rst) begin
        if (rst) begin
            state <= RESET;
            trade_req <= 1'b0;
        end else begin

            if (px_offset_valid) begin
                px_offset_latched <= px_offset;
            end
            trade_req <= 1'b0;

            // FSM
            state <= state;  // Remain in current state by default
            case (state)
                RESET: begin
                    state <= IDLE;
                    trade_req <= 1'b0;
                    // Not used in synthesis, but useful for verif.
                    px_offset_latched <= 'X;
                    packet_index <= 'X;
                    product_tcp <= 'X;
                    price_tcp <= 'X;
                    buy_nsell_tcp <= 'X;
                end

                IDLE: begin
                    if (tcp_sop) begin
                        state <= WAIT_FOR_PACKET_PRODUCT;
                        packet_index <= 'd1;
                    end
                end

                WAIT_FOR_PACKET_PRODUCT: begin
                    if (tcp_valid) begin
                        if (packet_index == I_PRODUCT_MSB) begin
                            product_tcp[15:8] <= tcp_data;
                        end
                        if (packet_index == I_PRODUCT_LSB) begin
                            product_tcp[7:0] <= tcp_data;
                            price_tcp <= '0;
                            state <= WAIT_FOR_PACKET_PRICE;
                        end
                        packet_index <= packet_index + 1'd1;
                    end
                end

                WAIT_FOR_PACKET_PRICE: begin
                    if (tcp_valid) begin
                        if (packet_index >= I_PRICE_MSB) begin
                            price_tcp <= (price_tcp << 8) | {24'd0, tcp_data};
                        end
                        if (packet_index == I_PRICE_LSB) begin
                            state <= WAIT_FOR_PACKET_BUY;
                        end
                        packet_index <= packet_index + 1'd1;
                    end
                end

                WAIT_FOR_PACKET_BUY: begin
                    if (tcp_valid) begin
                        if (packet_index == I_BUY_NSELL) begin
                            buy_nsell_tcp <= tcp_data[0];
                            state <= OUTPUT_TRADE;
                        end
                        packet_index <= packet_index + 1'd1;
                    end
                end

                OUTPUT_TRADE: begin
                    trade_req <= should_trade;
                    state <= (tcp_eop ? IDLE : WAIT_FOR_PACKET_END);
                end

                WAIT_FOR_PACKET_END: begin
                    if (tcp_eop) begin
                        state <= IDLE;
                    end
                end

                default: begin
                    state <= RESET;
                end
            endcase
        end
    end
endmodule

// I can only pray to the EDA gods that this infers block ram
module product_theo_table #(
    parameter integer PROD_BITS = 16,
    parameter integer THEO_BITS = 32
) (
    input  logic                    clk,        // Clock
    input  logic                    srst,       // Synchronous high reset
    input  logic                    save_theo,  // Save product & theo into table
    input  logic [PROD_BITS-1:0]    product,    // Product number for read/write from table
    input  logic [THEO_BITS-1:0]    theo_in,    // Theo to save to table (when `save_theo` asserted)
    output logic [THEO_BITS-1:0]    theo_out    // Theo output from previous cycle's `product_num`
);
    localparam integer MAX_PROD = (2**PROD_BITS - 1);

    logic [THEO_BITS-1:0] theo_array [MAX_PROD:0];

    initial begin
        for (integer i = 0; i <= MAX_PROD; i += 1) begin
            theo_array[i] = '0;
        end
    end

    always_ff @(posedge clk) begin
        if (srst) begin
            // Clearing memory on a reset is not something I am familiar with.
            // To my (albeit limited) knowledge, this isn't a typically supported
            // feature of FPGA memory modules. May be possible if you use some memory
            // that requires refreshing (e.g. DRAM), so it could be cleared in one go.
            // However, I'm going to skirt this requirement due to the following.
            //
            // Technically, the specs. mention that
            //   "A reset pulse must clear any saved theos in your module...".
            // However, it also states both that
            //   "The trader will always program all possible theos before the first market data message arrives.."
            //   "the trader will reprogram the theos before the next market data message."
            //
            // Hence, I assume it is SAFE to not reset memory or even keep track of
            // which product & theos are valid/programmed, because any product/theos
            // will be overwritten before data packets.
        end else begin
            if (save_theo) begin
                theo_array[product] <= theo_in;
            end
            // No read enable; just keep outputting theo for simplicity
            theo_out <= theo_array[product];
        end
    end
endmodule
