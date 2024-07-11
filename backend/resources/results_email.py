results_email_body = """
    <html>
        <body style="font-family: Arial, sans-serif; color: #333; font-size: 18px;">
            <div style="text-align: center; padding: 20px;">
                <img src="cid:logo" alt="FERNEC Logo" style="width: 200px;">
            </div>
            <div style="margin: 20px; text-align: center;">
                <h2 style="font-size: 24px;">Dear User,</h2>
                <p style="font-size: 20px;">We are pleased to inform you that your results are ready.</p>
                <p style="font-size: 20px;">Please click the link below to view them:</p>
                <a href="{0}" style="display: inline-block; padding: 12px 24px; background-color: #007BFF; 
                    color: #fff; text-decoration: none; border-radius: 5px; font-size: 20px;">View Results</a>
                <p style="font-size: 20px;">Sincerely,<br>The FERNEC Team</p>
            </div>
        </body>
    </html>
    """
