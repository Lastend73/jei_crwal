import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
# from important_data import get_app_password


HOST = "smtp-mail.outlook.com"
PORT = 587

def sendmail(info) : 
    from_addr = formataddr(('황규민','이메일'))
    password = "비밀번호"

    # 메일 본문
    msg = MIMEMultipart()
    msg['From'] = from_addr  # 송신자
    msg['To'] = "kyu233@jeisys.com" # join() 함수에 문자열을 직접 전달하는 것은 잘못된 사용법입니다
    msg["Subject"] = info # 제목

    body = info # 내용

    msg.attach(MIMEText(body,"plain"))

    try:
        session = smtplib.SMTP(HOST,PORT)
        session.ehlo()
        session.starttls()

        status_code, response = session.login('kyu233@jeisys.com',password)
        print(f"{status_code} : {response}")

        text = msg.as_string()
        session.sendmail(from_addr,'kyu233@jeisys.com',text)

    except smtplib.SMTPAuthenticationError:
        print("인증 오류: 이메일 주소나 비밀번호가 잘못되었습니다.")
    except smtplib.SMTPException as e:
        print(f"SMTP 오류 발생: {str(e)}")
    except Exception as e:
        print(f"기타 오류 발생: {str(e)}")
    finally:
        session.quit()