FROM kalilinux/kali-rolling

# Install necessary packages
RUN apt-get update && \
    apt-get install -y kali-desktop-core kali-desktop-live tigervnc-standalone-server

# Set up VNC password
RUN mkdir -p ~/.vnc && \
    echo "password" | vncpasswd -f > ~/.vnc/passwd && \
    chmod 600 ~/.vnc/passwd

# Expose VNC port
EXPOSE 5900

# Start VNC server
CMD ["vncserver", ":1", "-geometry", "1280x720", "-depth", "24"]
