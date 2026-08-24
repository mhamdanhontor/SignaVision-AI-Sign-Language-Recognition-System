import {
  describe,
  expect,
  it,
} from "vitest";


describe(
  "Prediction API response",
  () => {

    it(
      "uses the expected prediction structure",
      () => {

        const response = {
          prediction: "A",
          confidence: 0.997,
        };


        expect(response)
          .toHaveProperty(
            "prediction"
          );


        expect(response)
          .toHaveProperty(
            "confidence"
          );


        expect(
          typeof response.prediction
        ).toBe("string");


        expect(
          typeof response.confidence
        ).toBe("number");


        expect(
          response.confidence
        ).toBeGreaterThanOrEqual(0);


        expect(
          response.confidence
        ).toBeLessThanOrEqual(1);

      }
    );

  }
);