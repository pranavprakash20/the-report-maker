# the-report-maker
Python
HTML5
A simple yet powerful Python script that transforms your test automation results into beautiful, professional HTML reports with just a few lines of input.

🌟 Features
Transforms plain text test results into visually appealing HTML reports

Color-coded results (green for passes, red for failures)

Simple input format - just specify "test_name : result"

Lightweight with no external dependencies

Fully customizable HTML template

📥 Installation
Clone this repository:

bash
git clone https://github.com/pranavprakash20/the-report-maker.git
Navigate to the project directory:

bash
cd test-report-generator
� Usage
Basic Usage
Prepare your test results in the required format:

test_1 : pass
test_2 : failed
test_3 : pass
login_test : failed
performance_test : pass
Run the script with your test results:

bash
python report_generator.py (specify the input and output file in the python file)
Command Line Options
Option	Description	Example
	Input file containing test results	(eg: results.txt )
	Output HTML file name	(eg: my_report.html )


test_name : result
Where result can be:

pass or passed (case insensitive)

fail or failed (case insensitive)

Examples:

homepage_load_test : pass
login_functionality : failed
search_feature : Pass
checkout_process : FAILED

📊 Sample Report Preview
![alt text](https://github.com/pranavprakash20/the-report-maker/blob/main/sample_report.jpg?raw=true)


🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements.

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

✨ Transform your test results into beautiful reports with just one command! ✨
