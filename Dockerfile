# Use a base image that already has Node.js and Python, which are good starting points for Playwright
# This image includes Playwright dependencies and browsers
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set the working directory inside the container
WORKDIR /app

# Copy your project's requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container
# This step should be after installing requirements to optimize Docker caching
COPY . .

# If you have an entrypoint script (optional, but good for custom run commands)
# ENTRYPOINT ["python", "-m", "pytest"]

# Command to run by default if no command is specified when launching the container
# CMD ["/bin/bash"]