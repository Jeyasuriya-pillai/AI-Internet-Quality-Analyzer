import subprocess
import platform
import re
import statistics


def ping_host(host="1.1.1.1", count=10):
    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", str(count), host]
    else:
        command = ["ping", "-c", str(count), host]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout

        times = []

        if system == "windows":
            matches = re.findall(r"time[=<]\s*(\d+)ms", output, re.IGNORECASE)
        else:
            matches = re.findall(r"time[=<]\s*([\d.]+)\s*ms", output, re.IGNORECASE)

        for value in matches:
            times.append(float(value))

        sent_match = re.search(
            r"(?:Sent =|transmitted,)\s*(\d+)",
            output,
            re.IGNORECASE
        )

        lost_match = re.search(
            r"(?:Lost =)\s*(\d+)",
            output,
            re.IGNORECASE
        )

        if sent_match and lost_match:
            sent = int(sent_match.group(1))
            lost = int(lost_match.group(1))
        else:
            sent = count
            lost = count - len(times)

        packet_loss = (lost / sent * 100) if sent else 100

        if times:
            latency = statistics.mean(times)

            if len(times) > 1:
                differences = [
                    abs(times[i] - times[i - 1])
                    for i in range(1, len(times))
                ]
                jitter = statistics.mean(differences)
            else:
                jitter = 0
        else:
            latency = 999
            jitter = 999

        return {
            "latency": round(latency, 2),
            "jitter": round(jitter, 2),
            "packet_loss": round(packet_loss, 2)
        }

    except Exception as e:
        return {
            "latency": 999,
            "jitter": 999,
            "packet_loss": 100,
            "error": str(e)
        }