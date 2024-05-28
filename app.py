from flask import Flask, render_template, request
import requests
import smtplib

response = requests.get("https://api.npoint.io/674f5423f73deab1e9a7")
blog_data = response.json()

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("index.html",
                           blog_data=blog_data)


@app.route("/post/<int:post_id>")
def post_page(post_id):
    post = None
    for post_data in blog_data:
        if post_id == post_data['id']:
            post = post_data

    return render_template("post.html",
                           post=post
                           )


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/contact", methods=['POST', 'GET'])
def contact_page():
    if request.method == "POST":
        data = request.form

        name = data['name']
        email = data['email']
        print(email)
        phone = data['number']
        message = data['message']
        # sending mail
        send_msg = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nmessage: {message}"
        send_email = "nikhiltelase@gmail.com"
        result = send_mail(mail_id=send_email, user_msg=send_msg)

        # send a mail to uere for interection
        feedbaack_msg = "Thank You!\n\nThank you for reaching out. We'll get back to you as soon as possible!"
        send_mail(mail_id=email, user_msg=feedbaack_msg)

        return render_template("contact.html", user_feedback=result)
    else:
        return render_template("contact.html", user_feedback="Contact Me")


def send_mail(mail_id, user_msg):
    my_email = "nikhiltelase17@gmail.com"
    password = "qkqincjpvnknezcy"
    message = f"Subject: Blog web \n\n{user_msg}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()  # secure
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=[mail_id],
                                msg=message)
        return "Thanks For Contact Me"
    except Exception:
        return "Error, please try again"


if __name__ == "__main__":
    app.run(debug=True)
