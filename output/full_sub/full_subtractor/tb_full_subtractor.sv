module full_subtractor_tb;

    // Parameters
    

    // Signals
    
    reg 1 a;
    
    reg 1 b;
    
    reg 1 bin;
    
    
    wire 1 diff;
    
    wire 1 bout;
    

    // Device Under Test (DUT)
    full_subtractor dut (
        
        .a(a),
        
        .b(b),
        
        .bin(bin),
        
        .diff(diff),
        
        .bout(bout)
        
    );

    // Clock Generation
    

    // Monitor Changes
    initial begin
        $monitor("Time=%0t | a=%h b=%h bin=%h diff=%h bout=%h ", $time, a, b, bin, diff, bout);
    end

    // Stimulus Logic
    initial begin
        // Reset Phase
        

        
        // Combinational Stimulus
        
        #10 a = $random;
        
        #10 b = $random;
        
        #10 bin = $random;
        
        

        #50;
        $display("Simulation finished at time %0t", $time);
        $finish;
    end

endmodule