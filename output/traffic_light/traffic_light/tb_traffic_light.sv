module traffic_light_tb;

    // Parameters
    
    localparam S_GREEN = 2'b00;
    
    localparam S_YELLOW = 2'b01;
    
    localparam S_RED = 2'b10;
    

    // Signals
    
    reg 1 clk;
    
    reg 1 rst_n;
    
    reg 1 sensor_req;
    
    
    wire [1:0] light;
    
    wire 1 done_tick;
    

    // Device Under Test (DUT)
    traffic_light dut (
        
        .clk(clk),
        
        .rst_n(rst_n),
        
        .sensor_req(sensor_req),
        
        .light(light),
        
        .done_tick(done_tick)
        
    );

    // Clock Generation
    
    
    initial clk = 0;
    always #5 clk = ~clk;
    
    

    // Monitor Changes
    initial begin
        $monitor("Time=%0t | clk=%h rst_n=%h sensor_req=%h light=%h done_tick=%h ", $time, clk, rst_n, sensor_req, light, done_tick);
    end

    // Stimulus Logic
    initial begin
        // Reset Phase
        
        rst_n = 1;
        #20 rst_n = 0;
        

        
        // Sequential Stimulus
        repeat(5) @(posedge clk);
        
        
        sensor_req = $random;
        @(posedge clk);
        
        
        

        #50;
        $display("Simulation finished at time %0t", $time);
        $finish;
    end

endmodule