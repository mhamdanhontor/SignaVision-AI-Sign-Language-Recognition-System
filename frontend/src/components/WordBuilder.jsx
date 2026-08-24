import { useEffect, useRef, useState } from "react";


const LETTER_CLASSES = new Set(
  "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("")
);


function WordBuilder({
  stableSign,
  text,
  setText,
}) {



  const [lastAdded, setLastAdded] =
    useState(null);

  const lockedSignRef =
    useRef(null);


  // ========================================================
  // Process Stable Sign
  // ========================================================

useEffect(() => {

  if (!stableSign) {
    return;
  }


  // ------------------------------------------------------
  // NOTHING = release the current sign
  // ------------------------------------------------------

  if (
    stableSign === "nothing"
  ) {

    lockedSignRef.current =
      null;

    setLastAdded(
      "nothing"
    );

    return;
  }


  // ------------------------------------------------------
  // Same sign is still being held
  // ------------------------------------------------------

  if (
    lockedSignRef.current ===
    stableSign
  ) {
    return;
  }


    // ------------------------------------------------------
    // New sign detected
    // ------------------------------------------------------

    lockedSignRef.current =
      stableSign;


    // ------------------------------------------------------
    // Letter
    // ------------------------------------------------------

    if (
      LETTER_CLASSES.has(
        stableSign
      )
    ) {

      setText(
        (previous) =>
          previous + stableSign
      );

      setLastAdded(
        stableSign
      );

      return;
    }


    // ------------------------------------------------------
    // Space
    // ------------------------------------------------------

    if (
      stableSign === "space"
    ) {

      setText(
        (previous) => {

          if (
            previous.length === 0
          ) {
            return previous;
          }

          if (
            previous.endsWith(" ")
          ) {
            return previous;
          }

          return previous + " ";
        }
      );

      setLastAdded(
        "space"
      );

      return;
    }


    // ------------------------------------------------------
    // Delete
    // ------------------------------------------------------

    if (
      stableSign === "del"
    ) {

      setText(
        (previous) =>
          previous.slice(0, -1)
      );

      setLastAdded(
        "del"
      );

      return;
    }




  }, [stableSign]);


  // ========================================================
  // Unlock Sign
  // ========================================================

  const unlockSign = () => {

    lockedSignRef.current =
      null;
  };


  // ========================================================
  // Clear Text
  // ========================================================

  const clearText = () => {

    setText("");

    setLastAdded(null);

    lockedSignRef.current =
      null;
  };


  // ========================================================
  // Delete Last Character
  // ========================================================

  const deleteLastCharacter = () => {

    setText(
      (previous) =>
        previous.slice(0, -1)
    );

    lockedSignRef.current =
      null;

    setLastAdded("del");
  };


  // ========================================================
  // Copy Text
  // ========================================================

  const copyText = async () => {

    if (!text) {
      return;
    }

    try {

      await navigator.clipboard.writeText(
        text
      );

    } catch (error) {

      console.error(
        "Failed to copy text:",
        error
      );

    }
  };


  // ========================================================
  // Render
  // ========================================================

  return (
    <div className="card shadow-sm border-0">

      <div className="card-body p-4">

        <div className="d-flex justify-content-between align-items-center mb-3">

          <div>

            <h2 className="h5 fw-bold mb-1">
              ASL → Text
            </h2>

            <p className="text-secondary small mb-0">
              Your recognised signs appear here.
            </p>

          </div>

          <span className="badge bg-primary">
            {text.length} characters
          </span>

        </div>


        {/* =================================================
            Text Display
        ================================================= */}

        <div className="word-builder-display">

          {text ? (
            <span>
              {text}
            </span>
          ) : (
            <span className="text-secondary">
              Start showing signs...
            </span>
          )}

        </div>


        {/* =================================================
            Last Sign
        ================================================= */}

        <div className="d-flex justify-content-between align-items-center mt-3">

          <div className="small text-secondary">

            Last recognised:

            <strong className="ms-1 text-dark">

              {lastAdded || "—"}

            </strong>

          </div>


          {stableSign && (

            <div className="small">

              Stable:

              <span className="badge bg-success ms-1">

                {stableSign}

              </span>

            </div>

          )}

        </div>


        {/* =================================================
            Controls
        ================================================= */}

        <div className="row g-2 mt-3">

          <div className="col-4">

            <button
              className="btn btn-outline-danger w-100"
              onClick={
                deleteLastCharacter
              }
              disabled={!text}
            >

              <i className="bi bi-backspace me-1"></i>

              Delete

            </button>

          </div>


          <div className="col-4">

            <button
              className="btn btn-outline-secondary w-100"
              onClick={unlockSign}
            >

              <i className="bi bi-unlock me-1"></i>

              Unlock

            </button>

          </div>


          <div className="col-4">

            <button
              className="btn btn-outline-primary w-100"
              onClick={copyText}
              disabled={!text}
            >

              <i className="bi bi-copy me-1"></i>

              Copy

            </button>

          </div>

        </div>


        <button
          className="btn btn-outline-dark w-100 mt-2"
          onClick={clearText}
          disabled={!text}
        >

          <i className="bi bi-trash me-2"></i>

          Clear Text

        </button>

      </div>

    </div>
  );
}


export default WordBuilder;