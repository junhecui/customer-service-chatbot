from src.integrations.gmail import send_email

def test_send_email_success():
    print("Testing successful email sending...")

    to = "test@example.com"
    subject = "Test Email Success"
    message_text = "This is a test email to check successful email sending functionality."

    try:
        send_email(to, subject, message_text)
        print("Test passed: Email sent successfully.")
    except Exception as e:
        print("Test failed:", e)

def test_send_email_failure():
    print("Testing email sending failure...")

    to = "invalid-email"
    subject = "Test Email Failure"
    message_text = "This email should fail to send due to invalid email format."

    try:
        send_email(to, subject, message_text)
        print("Test failed: Email should not have been sent successfully with invalid email format.")
    except Exception as e:
        print("Test passed: Caught exception as expected:", e)

if __name__ == "__main__":
    print("Running email tests...\n")
    test_send_email_success()
    print("\n")
    test_send_email_failure()