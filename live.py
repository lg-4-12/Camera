from ultralytics import YOLO
import cv2

# Load the YOLO model
model = YOLO("./models/cat-v3-430-imgs.pt")

# Open the video stream
stream_url = 'tcp://100.70.0.2:8888'
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Error: Unable to open video stream.")
    exit()

while True:
    # Read a frame from the stream
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame.")
        break

    # Perform object detection
    results = model(frame)

    # Process detection results
    for result in results:
        # Loop through each detected object
        for box in result.boxes:
            # Extract bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            # Draw the bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Optional: Draw a label with the class name and probability
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            prob = box.conf[0]
            label = f"{class_name} {prob:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Preview", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()