from flask import Flask, request
from stock import check_engulfing_pattern
import re

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def adder_page():
    errors = ""
    if request.method == "POST":
        stock1 = None
        try:
            stock1 = str(request.form["stock1"])
            if not stock1:
                raise ValueError("<p>Stock name cannot be empty.</p>")
            elif not re.match("^[a-zA-Z0-9]+$", stock1):
                raise ValueError("<p>Invalid stock name. Only alphanumeric characters are allowed.</p>")
        except KeyError:
            errors += "<p>Stock name not provided.</p>"
        except ValueError as e:
            errors += str(e)
        if errors:
            html = "<html><body>"
            html += "<h1>Error:</h1>"
            html += errors
            html += "</body></html>"
            return html
        if stock1 is not None:
            result = check_engulfing_pattern(stock1)
            return '''
                <html>
                    <body>
                        <p>Here is what we think: {result}</p>
                        <p><a href="/">Click here to estimate again</a>
                    </body>
                </html>
            '''.format(result=result)

    return f'''
            <html>
            <head>
                <style>
                    /* Styles for mobile screens */
                    @media (max-device-width: 480px) {{
                        body {{
                            font-size: 40px;  /* Adjust the font size as desired */
                        }}
                        p, ul, li {{
                            padding: 5px;
                            word-wrap: break-word;  /* Allow lines to break */
                            border: 5px solid transparent;  /* Add border style */
                        }}
                        input[type="submit"] {{
                            font-size: 25px;  /* Adjust the font size as desired */
                            padding: 5px 10px;
                        }}
                        input[name="stock1"] {{
                            width: 100%;
                            padding: 10px;
                            font-size: 25px;
                        }}
                    }}

                    /* Additional styles for larger screens if needed */
                    @media (min-width: 481px) {{
                        /* Add your custom styles for larger screens here */
                    }}
                </style>
            </head>
            <body>
                {errors}
                <p>Enter the Indian Stock Market Symbol:</p>
                <form method="post" action=".">
                    <p><input name="stock1" /></p>
                    <p><input type="submit" value="Is it a good time to buy or sell?" /></p>
                </form>
                <br>
                <p>Indicators Used:</p>
                <ul>
                    <li>Bearish Engulfing: A bearish candlestick pattern that suggests a potential reversal of an uptrend.</li>
                    <li>Bullish Engulfing: A bullish candlestick pattern that suggests a potential reversal of a downtrend.</li>
                    <li>Current Price: The most recent trading price of the stock.</li>
                    <li>Moving Average: A smoothed average of stock prices over a specific period, used to identify trends.</li>
                    <li>RSI (Relative Strength Index): A technical indicator used to evaluate overbought or oversold conditions.</li>
                </ul>
                <br>
                <p>Warning:</p>
                <ul>
                    <li>This is a purely academic project. Please don't hold me responsible for any potential losses made using the info shown here.</li>
                    <li>Your decisions should be based on your intellect and research.</li>
                </ul>
            </body>
            </html>
        '''