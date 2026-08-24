export const getHandBoundingBox = (
  landmarks,
  videoWidth,
  videoHeight
) => {

  if (
    !landmarks ||
    !landmarks.length
  ) {
    return null;
  }


  let minX = 1;
  let minY = 1;
  let maxX = 0;
  let maxY = 0;


  landmarks.forEach(
    (landmark) => {

      minX = Math.min(
        minX,
        landmark.x
      );

      minY = Math.min(
        minY,
        landmark.y
      );

      maxX = Math.max(
        maxX,
        landmark.x
      );

      maxY = Math.max(
        maxY,
        landmark.y
      );
    }
  );


  let x =
    minX * videoWidth;

  let y =
    minY * videoHeight;

  let width =
    (maxX - minX) *
    videoWidth;

  let height =
    (maxY - minY) *
    videoHeight;


  // ------------------------------------------------------
  // Add padding around the hand
  // ------------------------------------------------------

  const paddingX =
    width * 0.25;

  const paddingY =
    height * 0.25;


  x -= paddingX;

  y -= paddingY;

  width +=
    paddingX * 2;

  height +=
    paddingY * 2;


  // ------------------------------------------------------
  // Keep crop inside video boundaries
  // ------------------------------------------------------

  x = Math.max(
    0,
    x
  );

  y = Math.max(
    0,
    y
  );


  width =
    Math.min(
      width,
      videoWidth - x
    );

  height =
    Math.min(
      height,
      videoHeight - y
    );


  return {
    x,
    y,
    width,
    height,
  };
};


export const cropHandToCanvas = (
  video,
  canvas,
  boundingBox
) => {

  if (!boundingBox) {
    return false;
  }


  const {
    x,
    y,
    width,
    height,
  } = boundingBox;


  const size =
    Math.max(
      width,
      height
    );


  const centerX =
    x + width / 2;

  const centerY =
    y + height / 2;


  let cropX =
    centerX - size / 2;

  let cropY =
    centerY - size / 2;


  cropX =
    Math.max(
      0,
      cropX
    );

  cropY =
    Math.max(
      0,
      cropY
    );


  if (
    cropX + size >
    video.videoWidth
  ) {

    cropX =
      video.videoWidth -
      size;
  }


  if (
    cropY + size >
    video.videoHeight
  ) {

    cropY =
      video.videoHeight -
      size;
  }


  cropX =
    Math.max(
      0,
      cropX
    );

  cropY =
    Math.max(
      0,
      cropY
    );


  canvas.width =
    128;

  canvas.height =
    128;


  const context =
    canvas.getContext(
      "2d",
      {
        willReadFrequently: true,
      }
    );


  context.clearRect(
    0,
    0,
    128,
    128
  );


  context.drawImage(
    video,

    cropX,
    cropY,
    size,
    size,

    0,
    0,
    128,
    128
  );


  return true;
};