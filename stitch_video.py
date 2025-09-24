import cv2
import os
import time
import math

def extract_frames(video_path, output_dir, step=10):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    saved_frames = []

    if not cap.isOpened():
        print("❌ Could not open video.")
        return []

    os.makedirs(output_dir, exist_ok=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % step == 0:
            frame_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_frames.append(frame_path)
        frame_count += 1

    cap.release()
    print(f"✅ Extracted {len(saved_frames)} frames with step={step}")
    return saved_frames

def stitch_images(image_paths, scale=0.5):
    if len(image_paths) < 2:
        return None, None

    images = []
    for p in image_paths:
        img = cv2.imread(p)
        if img is None:
            continue
        img = cv2.resize(img, (0,0), fx=scale, fy=scale)
        images.append(img)

    if len(images) < 2:
        return None, None

    stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
    start = time.time()
    status, pano = stitcher.stitch(images)
    elapsed = time.time() - start

    if status != cv2.Stitcher_OK:
        return None, elapsed

    return pano, elapsed

if __name__ == "__main__":
    video_path = "'/Users/rohankilaru/Drone Project #1/Minecraft_stitch_test.mp4'"
    frames_dir = "/Users/rohankilaru/frames"
    scale = 0.5

    best_panorama = None
    best_step = None
    best_nframes = None
    best_time = None

    # ---------------- Dynamic step generation ----------------
    # Start at 2, multiply by 1.5 until 10 or total frames
    max_step = 10
    step = 2
    steps_to_try = []
    while step <= max_step:
        steps_to_try.append(math.floor(step))
        step *= 1.5
    steps_to_try = sorted(list(set(steps_to_try)))  # remove duplicates
    print(f"Steps to try: {steps_to_try}")

    # ---------------- Dynamic nframes generation ----------------
    # Will generate [4,6,8,...] up to total frames (we determine after extraction)
    # placeholder, actual nframes generated per step after extraction
    nframes_to_try = None  

    for step in steps_to_try:
        frame_paths = extract_frames(video_path, frames_dir, step=step)
        if not frame_paths:
            continue

        total_frames = len(frame_paths)
        nframes_to_try = list(range(4, total_frames+1, 2))  # 4,6,8,... up to total frames

        for n in nframes_to_try:
            subset = frame_paths[:n]
            print(f"\n⚡ Trying step={step}, frames={n}")
            pano, elapsed = stitch_images(subset, scale=scale)

            if elapsed is not None and elapsed > 1.0:
                print(f"⏱ Stitching took {elapsed:.2f}s > 1s → stopping further attempts.")
                break  # Stop trying higher nframes for this step

            if pano is not None:
                print(f"✅ Success with {n} frames in {elapsed:.2f}s")
                # Keep the largest frame count under 1s
                if best_nframes is None or n > best_nframes:
                    best_panorama = pano
                    best_step = step
                    best_nframes = n
                    best_time = elapsed

        # Stop trying higher steps if we already have a fast working panorama
        if best_panorama is not None and best_time <= 1.0:
            break

    if best_panorama is not None:
        out_path = "/Users/rohankilaru/panorama_fast_dynamic.jpg"
        cv2.imwrite(out_path, best_panorama)
        print(f"\n🏆 Best panorama saved to {out_path}")
        print(f"   → step={best_step}, frames={best_nframes}, time={best_time:.2f}s")
    else:
        print("❌ Could not create a panorama under 1 second.")
