# Official Playwright image comes with browsers and OS deps pre-installed
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set the working directory inside the container
WORKDIR /app

# Copy and install requirements first to leverage Docker caching
COPY requirements.txt .
# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container
COPY . .

# ENTRYPOINT ["python", "-m", "pytest"]

# Command to run by default if no command is specified when launching the container
# CMD ["/bin/bash"]