import cv2
# from flask import Flask
# from flask import Response
# from flask import render_template
# import threading
#
# outputFrame = None
# lock = threading.Lock()
#
# app = Flask(__name__)

def main():
    cap = cv2.VideoCapture("http://10.0.0.167:81/stream")
    # cap = cv2.VideoCapture(0)
    render_loop(cap)
    cap.release()
    cv2.destroyAllWindows()

def render_loop(cap):
    _, prev_frame = cap.read()
    while not pressed_esc():
        prev_frame = display_delta_and_update_frame(cap, prev_frame)

def display_delta_and_update_frame(cap, prev_frame):
    global outputFrame, lock
    _, new_frame = cap.read()
    diff_frame = cv2.absdiff(src1=new_frame, src2=prev_frame)
    cv2.imshow('webcam', diff_frame)
    # with lock:
    #     outputFrame = diff_frame.copy()
    return new_frame

def pressed_esc():
    return cv2.waitKey(30) == 27

# @app.route("/")
# def index():
# 	return render_template("index.html")
#
# def generate():
#     global outputFrame, lock
#     while True:
#         with lock:
#             if outputFrame is None:
#                 continue
#             (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
#             # if not flag:
#             #     continue
#             yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
#
# @app.route("/video_feed")
# def video_feed():
# 	return Response(generate(),
# 		mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    # t = threading.Thread(target=main)
    # t.daemon = True
    # t.start()
    # app.run(host='localhost', port=8000, debug=True, threaded=True, use_reloader=False)
    main()
