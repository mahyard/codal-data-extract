FROM python:3.12-alpine as base

ARG PRJ_ROOT=/workspace
WORKDIR $PRJ_ROOT/source
ENV VIRTUAL_ENV=$PRJ_ROOT/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apk add --no-cache curl ca-certificates \
    && update-ca-certificates

RUN adduser -S -h $PRJ_ROOT -u 1001 nonroot
RUN chown -R nonroot: $PRJ_ROOT

#####
FROM base as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python3 -m venv $VIRTUAL_ENV

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

#####
FROM base as runner

USER nonroot

# Set the environment variables
# ENV FLASK_APP=webservice.py

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

# Copy the Flask app code into the container
COPY webservice.py .

# Run the Flask app
CMD ["python", "webservice.py"]
