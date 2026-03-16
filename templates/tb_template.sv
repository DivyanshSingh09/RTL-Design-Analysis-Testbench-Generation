module {{ name }}_tb;

    // Parameters
    {% for param, value in parameters.items() %}
    localparam {{ param }} = {{ value }};
    {% endfor %}

    // Signals
    {% for port in inputs %}
    reg {{ port.width if port.width != 1 else '' }} {{ port.name }};
    {% endfor %}
    {% for port in outputs %}
    wire {{ port.width if port.width != 1 else '' }} {{ port.name }};
    {% endfor %}

    // Device Under Test (DUT)
    {{ name }} dut (
        {% for port in inputs + outputs %}
        .{{ port.name }}({{ port.name }}){{ "," if not loop.last else "" }}
        {% endfor %}
    );

    // Clock Generation
    {% if clocks %}
    {% for clk in clocks %}
    initial {{ clk }} = 0;
    always #5 {{ clk }} = ~{{ clk }};
    {% endfor %}
    {% endif %}

    // Monitor Changes
    initial begin
        $monitor("Time=%0t | {% for port in inputs + outputs %}{{ port.name }}=%h {% endfor %}", $time, {% for port in inputs + outputs %}{{ port.name }}{{ ", " if not loop.last else "" }}{% endfor %});
    end

    // Stimulus Logic
    initial begin
        // Reset Phase
        {% for rst in resets %}
        {{ rst }} = 1;
        #20 {{ rst }} = 0;
        {% endfor %}

        {% if clocks %}
        // Sequential Stimulus
        repeat(5) @(posedge {{ clocks[0] }});
        
        {% for port in inputs if port.name not in clocks and port.name not in resets %}
        {{ port.name }} = $random;
        @(posedge {{ clocks[0] }});
        {% endfor %}
        
        {% else %}
        // Combinational Stimulus
        {% for port in inputs %}
        #10 {{ port.name }} = $random;
        {% endfor %}
        {% endif %}

        #50;
        $display("Simulation finished at time %0t", $time);
        $finish;
    end

endmodule