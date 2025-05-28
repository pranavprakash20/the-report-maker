import os
from datetime import datetime
from collections import defaultdict


def parse_test_results (file_path):
    """
    Parse the test results from the text file.
    Expected format: "Test Name : Status" (pass or failed)
    """
    test_results = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    test_name, status = map(str.strip, line.split(':'))
                    test_results.append({
                        'name': test_name,
                        'status': status.lower(),
                        'class': 'success' if status.lower() == 'pass' else 'danger'
                    })
                except ValueError:
                    print(f"Skipping malformed line: {line}")
    return test_results


def generate_html_report (test_results, output_file='test_report.html'):
    """
    Generate an advanced HTML report from the test results
    """
    # Calculate statistics
    total_tests = len(test_results)
    passed_tests = sum(1 for test in test_results if test['status'] == 'pass')
    failed_tests = total_tests - passed_tests
    print(failed_tests)
    pass_percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    fail_percentage = 100 - pass_percentage

    # Group tests by status for the details section
    tests_by_status = defaultdict(list)
    for test in test_results:
        tests_by_status[test['status']].append(test)

    # Get current timestamp for the report
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # HTML template with embedded CSS and JavaScript
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Test Execution Report</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f8f9fa;
                color: #333;
            }}
            .report-header {{
                background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
                color: white;
                padding: 2rem 0;
                margin-bottom: 2rem;
                border-radius: 0 0 10px 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .summary-card {{
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s;
                margin-bottom: 20px;
            }}
            .summary-card:hover {{
                transform: translateY(-5px);
            }}
            .chart-container {{
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }}
            .test-details {{
                margin-top: 20px;
            }}
            .accordion-button:not(.collapsed) {{
                background-color: rgba(106, 17, 203, 0.1);
                color: #6a11cb;
            }}
            .test-pass {{
                background-color: rgba(40, 167, 69, 0.1) !important;
            }}
            .test-fail {{
                background-color: rgba(220, 53, 69, 0.1) !important;
            }}
            .badge-summary {{
                font-size: 1rem;
                padding: 0.5em 0.75em;
            }}
            .footer {{
                background-color: #343a40;
                color: white;
                padding: 1rem 0;
                margin-top: 2rem;
                text-align: center;
            }}
            .status-icon {{
                margin-right: 8px;
            }}
        </style>
    </head>
    <body>
        <!-- Header -->
        <div class="report-header text-center">
            <div class="container">
                <h1><i class="fas fa-clipboard-check status-icon"></i> Test Execution Report</h1>
                <p class="lead">Generated on {timestamp}</p>
            </div>
        </div>

        <div class="container">
            <!-- Summary Cards -->
            <div class="row">
                <div class="col-md-4">
                    <div class="card summary-card bg-light">
                        <div class="card-body text-center">
                            <h3 class="card-title"><i class="fas fa-list-ol text-primary"></i> Total Tests</h3>
                            <h2 class="display-4">{total_tests}</h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card summary-card bg-light">
                        <div class="card-body text-center">
                            <h3 class="card-title"><i class="fas fa-check-circle text-success"></i> Passed</h3>
                            <h2 class="display-4">{passed_tests}</h2>
                            <span class="badge bg-success badge-summary">{pass_percentage:.1f}%</span>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card summary-card bg-light">
                        <div class="card-body text-center">
                            <h3 class="card-title"><i class="fas fa-times-circle text-danger"></i> Failed</h3>
                            <h2 class="display-4">{failed_tests}</h2>
                            <span class="badge bg-danger badge-summary">{fail_percentage:.1f}%</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Charts -->
            <div class="row">
                <div class="col-md-6">
                    <div class="chart-container">
                        <h3><i class="fas fa-chart-pie text-primary"></i> Test Results Distribution</h3>
                        <canvas id="pieChart"></canvas>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="chart-container">
                        <h3><i class="fas fa-chart-bar text-primary"></i> Results Overview</h3>
                        <canvas id="barChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Test Details -->
            <div class="test-details">
                <h3><i class="fas fa-file-alt text-primary"></i> Test Details</h3>
                <div class="accordion" id="testAccordion">
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="headingPassed">
                            <button class="accordion-button test-pass" type="button" data-bs-toggle="collapse" data-bs-target="#collapsePassed" aria-expanded="true" aria-controls="collapsePassed">
                                <i class="fas fa-check-circle text-success status-icon"></i> Passed Tests ({passed_tests})
                            </button>
                        </h2>
                        <div id="collapsePassed" class="accordion-collapse collapse show" aria-labelledby="headingPassed" data-bs-parent="#testAccordion">
                            <div class="accordion-body">
                                <ul class="list-group">
                                    {"".join(f'<li class="list-group-item list-group-item-success"><i class="fas fa-check text-success"></i> {test["name"]}</li>' for test in tests_by_status.get("pass", []))}
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="headingFailed">
                            <button class="accordion-button test-fail collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFailed" aria-expanded="false" aria-controls="collapseFailed">
                                <i class="fas fa-times-circle text-danger status-icon"></i> Failed Tests ({failed_tests})
                            </button>
                        </h2>
                        <div id="collapseFailed" class="accordion-collapse collapse" aria-labelledby="headingFailed" data-bs-parent="#testAccordion">
                            <div class="accordion-body">
                                <ul class="list-group">
                                    {"".join(f'<li class="list-group-item list-group-item-danger"><i class="fas fa-times text-danger"></i> {test["name"]}</li>' for test in tests_by_status.get("failed", []))}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <div class="container">
                <p class="mb-0">Generated by Test Automation Framework</p>
                <p class="mb-0"><small>Report generated at {timestamp}</small></p>
            </div>
        </div>

        <!-- JavaScript for Charts -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Pie Chart
            const pieCtx = document.getElementById('pieChart').getContext('2d');
            const pieChart = new Chart(pieCtx, {{
                type: 'pie',
                data: {{
                    labels: ['Passed', 'Failed'],
                    datasets: [{{
                        data: [{passed_tests}, {failed_tests}],
                        backgroundColor: ['#28a745', '#dc3545'],
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                        }}
                    }}
                }}
            }});

            // Bar Chart
            const barCtx = document.getElementById('barChart').getContext('2d');
            const barChart = new Chart(barCtx, {{
                type: 'bar',
                data: {{
                    labels: ['Test Results'],
                    datasets: [
                        {{
                            label: 'Passed',
                            data: [{passed_tests}],
                            backgroundColor: '#28a745',
                            borderWidth: 1
                        }},
                        {{
                            label: 'Failed',
                            data: [{failed_tests}],
                            backgroundColor: '#dc3545',
                            borderWidth: 1
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        x: {{
                            stacked: true,
                        }},
                        y: {{
                            stacked: true,
                            beginAtZero: true,
                            max: {total_tests + 5 if total_tests > 0 else 10}
                        }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """

    # Write the HTML report to file
    with open(output_file, 'w') as file:
        file.write(html_template)

    print(f"HTML report generated successfully: {os.path.abspath(output_file)}")


def main ():
    # Get the input file path from user or use default
    input_file = "weekly_regression.txt"

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    # Parse the test results
    test_results = parse_test_results(input_file)

    if not test_results:
        print("No valid test results found in the file.")
        return

    # Generate the HTML report
    output_file = "test_report.html"
    generate_html_report(test_results, output_file)


if __name__ == "__main__":
    main()
