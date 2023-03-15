from flask import Flask,request

app=Flask(__name__)

@app.route('/',methods=["GET","POST"])

def plagiarism_detect():
    if request.method=="POST":
        pass
    return '''hello'''







if __name__=="__main__":
    app.run(debug=True)