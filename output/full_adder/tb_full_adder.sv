module full_adder_tb;

    // Parameters
    

    // Signals
    
    reg  a;
    
    reg  b;
    
    reg  cin;
    
    
    wire  sum;
    
    wire  cout;
    

    // Device Under Test (DUT)
    full_adder dut (
        
        .a(a),
        
        .b(b),
        
        .cin(cin),
        
        .sum(sum),
        
        .cout(cout)
        
    );

    // Clock Generation
    

    // Monitor Changes
    initial begin
        $monitor("Time=%0t | a=%h b=%h cin=%h sum=%h cout=%h ", $time, a, b, cin, sum, cout);
    end

    // Stimulus Logic
    initial begin
        // Reset Phase
        

        
        // Combinational Stimulus
        
        #10 a = $random;
        
        #10 b = $random;
        
        #10 cin = $random;
        
        

        #50;
        $display("Simulation finished at time %0t", $time);
        $finish;
    end

endmodule