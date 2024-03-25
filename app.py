# from flask import Flask, render_template
# import docker

# app = Flask(__name__)
# docker_client = docker.from_env()

# # HTML template for displaying the VNC viewer
# vnc_viewer_template = """
# <!DOCTYPE html>
# <html>
# <head>
#   <title>Kali Linux GUI</title>
#   <script src="https://unpkg.com/noVNC"></script>
#   <script>
#     window.addEventListener('load', function () {
#       var vnc = new RFB(document.getElementById('vnc'), '%s');
#       vnc.connect('%s', %s);
#     });
#   </script>
# </head>
# <body>
#   <h1>Kali Linux GUI</h1>
#   <div id="vnc" style="width: 800px; height: 600px;"></div>
# </body>
# </html>
# """

# def pull_kali_image():
#     try:
#         docker_client.images.get('kalilinux/kali-rolling')
#     except docker.errors.ImageNotFound:
#         print("Kali Linux image not found. Pulling...")
#         docker_client.images.pull('kalilinux/kali-rolling')

# @app.route('/start_lab')
# def start_lab():
#     pull_kali_image()
    
#     # Create a Docker container running Kali Linux with a VNC server
#     container = docker_client.containers.run(
#         'kalilinux/kali-rolling',
#         detach=True,
#         ports={'5900/tcp': ('127.0.0.1',)},
#     )
    
#     # Get the IP address of the container
#     ip_address = container.attrs['NetworkSettings']['IPAddress']
    
#     # Render the VNC viewer template with the container's IP address and port
#     vnc_url = f'http://{ip_address}:5900'
#     return render_template('vnc_viewer.html', vnc_url=vnc_url)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template
import docker

app = Flask(__name__)
docker_client = docker.from_env()

# HTML template for displaying the VNC viewer
vnc_viewer_template = """
<!DOCTYPE html>
<html>
<head>
  <title>Kali Linux GUI</title>
  <script src="https://unpkg.com/noVNC"></script>
  <script>
    window.addEventListener('load', function () {
      var vnc = new RFB(document.getElementById('vnc'), 'ws://localhost:5900/websockify');
      vnc.connect('ws://localhost:5900/websockify');
    });
  </script>
</head>
<body>
  <h1>Kali Linux GUI</h1>
  <div id="vnc" style="width: 800px; height: 600px;"></div>
</body>
</html>
"""

def pull_kali_image():
    try:
        docker_client.images.get('kalilinux/kali-rolling')
    except docker.errors.ImageNotFound:
        print("Kali Linux image not found. Pulling...")
        docker_client.images.pull('kalilinux/kali-rolling')

@app.route('/start_lab')
def start_lab():
    pull_kali_image()
    
    # Create a Docker container running Kali Linux with a VNC server
    container = docker_client.containers.run(
        'kalilinux/kali-rolling',
        detach=True,
        ports={'5900/tcp': ('127.0.0.1',)},
    )
    
    # Render the VNC viewer template
    return vnc_viewer_template

if __name__ == '__main__':
    app.run(debug=True)

