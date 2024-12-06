import speedtest
import time
import statistics
import socket
import threading
def get_server():
    """Retrieve and return the best server information."""
    try:
        st = speedtest.Speedtest()
        server = st.get_best_server()
        return server
    except speedtest.ConfigRetrievalError as e:
        return f" Error retrieving server configuration: {e}"
    except socket.gaierror as e:
        return f" DNS resolution error: {e}"
    except Exception as e:
        return f" An unexpected error occurred: {e}"

def get_downspeed():
    """Test and return the download speed in Mbps."""
    try:
        st = speedtest.Speedtest()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        return download_speed
    except Exception as e:
        return f" An error occurred during download speed test: {e}"

def get_upspeed():
    """Test and return the upload speed in Mbps."""
    try:
        st = speedtest.Speedtest()
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        return upload_speed
    except Exception as e:
        return f" An error occurred during upload speed test: {e}"

def get_ping():
    """Measure and return the ping value in ms."""
    try:
        st = speedtest.Speedtest()
        st.get_best_server()  # Make sure the server is selected
        ping = st.results.ping
        return ping
    except Exception as e:
        return f" An error occurred during ping measurement: {e}"

def get_jitter():
    """Measure and return the jitter value in ms."""
    try:
        st = speedtest.Speedtest()
        st.get_best_server()  # Make sure the server is selected
        ping_times = []

        def ping_test():
            ping = st.results.ping
            ping_times.append(ping)

        threads = []
        for _ in range(10):  # Take 10 ping samples
            thread = threading.Thread(target=ping_test)
            thread.start()
            threads.append(thread)
            time.sleep(0.02)  # Small delay between starting threads

        for thread in threads:
            thread.join()

        # Calculate jitter as the standard deviation of ping times
        jitter = statistics.stdev(ping_times) if len(ping_times) > 1 else 0
        return jitter
    except Exception as e:
        return f" An error occurred during jitter measurement: {e}"