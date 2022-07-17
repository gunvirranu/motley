`timescale 1ns / 1ps

module top_tb ();
    logic           clk;
    logic           areset;
    logic [15:0]    product_num;
    logic [31:0]    product_theo;
    logic           product_theo_valid;
    logic [7:0]     tcp_data;
    logic           tcp_valid;
    logic           tcp_sop;
    logic           tcp_eop;
    logic [31:0]    px_offset;
    logic           px_offset_valid;
    logic           trade;

    trading_engine trading_engine_inst (
        .clk                ( clk                   ),
        .rst                ( areset                ),
        .product_num        ( product_num           ),
        .product_theo       ( product_theo          ),
        .product_theo_valid ( product_theo_valid    ),
        .tcp_data           ( tcp_data              ),
        .tcp_valid          ( tcp_valid             ),
        .tcp_sop            ( tcp_sop               ),
        .tcp_eop            ( tcp_eop               ),
        .px_offset          ( px_offset             ),
        .px_offset_valid    ( px_offset_valid       ),
        .trade              ( trade                 )
    );

    bit[15:0] products[];
    bit[31:0] theos[];

    initial begin
        $dumpfile("top_tb.vcd");
        $dumpvars(0, trading_engine_inst);
        clk = 1;
        areset = 1;
        product_theo_valid = 0;
        px_offset_valid = 0;
        tcp_valid = 0;
        tcp_sop = 0;
        tcp_eop = 0;
        #2 areset = 0; #2

        #10
        program_price_offset(45);
        products = '{4321, 9999};
        theos = '{550, 5000};
        program_theos();
        send_market_tcp_packet(45, 4321, 800, 1);

        program_price_offset(100);
        products = '{ 3, 0, 11, 29, 100 };
        theos = '{ 10, 571, 1599, 9999, 98765432 };
        program_theos();
        send_market_tcp_packet(50, 0, 500, 0);
        send_market_tcp_packet(45, 11, 1599-101, 0);
        send_market_tcp_packet(42, 29, 9999+99, 0);
        send_market_tcp_packet(42, 100, 98765432-200, 0);
        send_market_tcp_packet(42, 100, 98765432-50, 0);
        send_market_tcp_packet(42, 100, 98765432+50, 0);
        send_market_tcp_packet(42, 100, 98765432+50, 1);
        send_market_tcp_packet(42, 100, 98765432+200, 1);
        program_price_offset(30);
        send_market_tcp_packet(42, 100, 98765432+50, 1);
        products = '{ 100 };
        theos = '{ 10000 };
        program_theos();
        send_market_tcp_packet(42, 100, 9980, 0);
        send_market_tcp_packet(42, 100, 10050, 1);

        #10; $finish;
    end

    task program_price_offset(
        input bit[31:0] price
    ); begin
        px_offset = price;
        px_offset_valid = 1;
        #2;
        px_offset_valid = 0;
        px_offset = 'X;
    end endtask

    task program_theos; begin
        for (integer i = 0; i < products.size(); i += 1) begin
            product_num = products[i];
            product_theo = theos[i];
            product_theo_valid = 1;
            #2;
            product_theo_valid = 0;
            product_num = 'X;
            product_theo = 'X;
        end
    end endtask

    task send_market_tcp_packet(
        input integer   TOTAL_PACKET_LEN,
        input bit[15:0] product,
        input bit[31:0] price,
        input bit       buy_nsell
    ); begin
        tcp_sop = 1;
        for (integer i = 0; i < TOTAL_PACKET_LEN; i += 1) begin
            case (i)
                30: tcp_data = product[15:8];
                31: tcp_data = product[7:0];
                34: tcp_data = price[31:24];
                35: tcp_data = price[23:16];
                36: tcp_data = price[15:8];
                37: tcp_data = price[7:0];
                40: tcp_data = {7'b0, buy_nsell};
                default: tcp_data = 8'b0;
            endcase
            tcp_valid = 1;
            #2;
            tcp_sop = 0;
        end
        tcp_valid = 0;
        tcp_eop = 1;
        #2 tcp_eop = 0;
    end endtask

    always begin
      #1 clk = ~clk;
    end
endmodule
