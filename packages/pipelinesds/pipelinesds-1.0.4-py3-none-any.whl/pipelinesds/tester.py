import pandas as pd

from evidently.test_suite import TestSuite
from evidently.report import Report
from evidently import tests, metrics, ColumnMapping

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def test_data(current_data,reference_data, config_file, stage):
    """
    Function to test data for issues.   

    Parameters
    ----------
    current_data: pd.DataFrame
        Current data to test.
    reference_data: pd.DataFrame
        Reference data.
    tests_config_file: dict
        Tests configuration file.
    stage: str
        Stage of the pipeline (either 'test_input' or 'test_output').

    Returns
    ----------
    pd.DataFrame
        Test results.
    """

    mapping = config_file[stage]['mapping']

    column_mapping = ColumnMapping(
        numerical_features=mapping.get('numerical_features', []),
        categorical_features=mapping.get('categorical_features', [])
    )

    tests_parsed = []

    for test in config_file[stage]['tests']:
        test_class = getattr(tests, test['type'])
        test_params = test['params']
        tests_parsed.append(test_class(**test_params))
            
    test_suite = TestSuite(tests=tests_parsed)

    test_suite.run(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)
    test_results = test_suite.as_dict()

    data = {}
    for test in test_results['tests']:
        column_name = test['name']
        data[column_name] = {
            'STATUS': test['status'],
            'CONDITION': test['parameters']['condition'],
            'VALUE': test['parameters']['value'],
            'COLUMN': test['parameters'].get('column_name', 'all columns')
        }

    test_frame = pd.DataFrame.from_dict(data, orient='index')
    test_frame.reset_index(inplace=True)
    test_frame.rename(columns={'index': 'TEST'}, inplace=True)

    return test_frame

def check_data_drift(current_data,reference_data, config_file):
    """
    Function to check data for drift.   

    Parameters
    ----------
    current_data: pd.DataFrame
        Current data to check.
    reference_data: pd.DataFrame
        Reference data.
    config_file: dict
        Tests configuration file.

    Returns
    ----------
    pd.DataFrame
        Test results.
    """

    mapping = config_file['drift']['mapping']

    column_mapping = ColumnMapping(
        numerical_features=mapping.get('numerical_features', []),
        categorical_features=mapping.get('categorical_features', [])
    )

    metrics_parsed = []

    for metric in config_file['drift']['metrics']:
        metric_class = getattr(metrics, metric['type'])
        metric_params = metric['params']
        metrics_parsed.append(metric_class(**metric_params))
            
    report = Report(metrics=metrics_parsed)

    report.run(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)
    report_results = report.as_html()

    data = {}
    for metric in report_results['metrics']:
        column_name = metric['name']
        data[column_name] = {
            'STATUS': metric['status'],
            'CONDITION': metric['parameters']['condition'],
            'VALUE': metric['parameters']['value'],
            'COLUMN': metric['parameters'].get('column_name', 'all columns')
        }

    report_frame = pd.DataFrame.from_dict(data, orient='index')
    report_frame.reset_index(inplace=True)
    report_frame.rename(columns={'index': 'METRIC'}, inplace=True)

    return report_frame

def send_email_with_table(credentials_frame, subject, html_table, receiver_email):
    """
    Function to send email with html table.   

    Parameters
    ----------
    credentials_frame: pd.DataFrame
        Dataframe with credentials.
    subject: str
        Subject of the email.
    html_table: str
        Data to send in the email.
    receiver_email: str
        Email address to send the email to.
    """

    credentials_dict = pd.Series(credentials_frame.setting_value.values, index=credentials_frame.setting_name).to_dict()

    sender_password=credentials_dict.get('MAIL_PASSWORD')
    sender_email=credentials_dict.get('MAIL_SENDER')
    sender_login=credentials_dict.get('MAIL_LOGIN')
    mail_host=credentials_dict.get('MAIL_HOST')
    mail_port=int(credentials_dict.get('MAIL_PORT'))

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_table, 'html'))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(mail_host, mail_port, context=context) as server:
        server.login(sender_login, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())