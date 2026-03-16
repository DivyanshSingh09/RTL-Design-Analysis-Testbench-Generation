module half_subtractor_tb;

    // Parameters
    

    // Signals
    
    reg 1 a;
    
    reg 1 b;
    
    
    wire 1 diff;
    
    wire 1 borrow;
    

    // Device Under Test (DUT)
    half_subtractor dut (
        
        .a(a),
        
        .b(b),
        
        .diff(diff),
        
        .borrow(borrow)
        
    );

    // Clock Generation
    

    // Monitor Changes
    initial begin
        $monitor("Time=%0t | a=%h b=%h diff=%h borrow=%h ", $time, a, b, diff, borrow);
    end

    // Stimulus Logic
    initial begin
        // Reset Phase
        

        
        // Combinational Stimulus
        
        #10 a = $random;
        
        #10 b = $random;
        
        

        #50;
        $display("Simulation finished at time %0t", $time);
        $finish;
    end

endmodule