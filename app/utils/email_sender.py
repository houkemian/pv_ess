import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

def send_otp_email(to_email: str, otp_code: str):
    """
    发送带有高质感 HTML 样式的 6 位验证码邮件
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        print("⚠️ 邮件发送失败：未配置 SMTP 环境变量。")
        return

    # 1. 构造邮件对象
    msg = MIMEMultipart()
    msg['From'] = f"Quote Master <{SMTP_USER}>" # 发件人显示名称
    msg['To'] = to_email
    msg['Subject'] = "[Quote Master] 您的密码重置验证码"

    # 2. 商业级 HTML 邮件模板
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f4f5; padding: 20px;">
        <div style="max-width: 500px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
          <h2 style="color: #1E293B; text-align: center;">重置您的密码</h2>
          <p style="color: #475569; font-size: 16px;">您好，</p>
          <p style="color: #475569; font-size: 16px;">我们收到了您重置密码的请求。您的验证码是：</p>
          <div style="text-align: center; margin: 30px 0;">
            <span style="display: inline-block; font-size: 32px; font-weight: bold; color: #00E676; background-color: #1E293B; padding: 10px 30px; border-radius: 8px; letter-spacing: 5px;">
              {otp_code}
            </span>
          </div>
          <p style="color: #475569; font-size: 14px;">此验证码在 <strong>15 分钟</strong> 内有效。如果您没有请求重置密码，请忽略此邮件。</p>
          <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;" />
          <p style="color: #94a3b8; font-size: 12px; text-align: center;">Quote Master PV+ESS Team</p>
        </div>
      </body>
    </html>
    """
    
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))

    # 3. 连接 SMTP 服务器并发送
    try:
        # 使用 SSL 加密端口 465
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"✅ 真实验证码 {otp_code} 已成功发送至 {to_email}")
    except Exception as e:
        print(f"❌ 邮件发送彻底失败: {e}")