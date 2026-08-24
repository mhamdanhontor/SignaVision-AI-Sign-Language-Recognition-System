import {
  describe,
  expect,
  it,
} from "vitest";

import {
  getHandBoundingBox,
} from "./cropHand";


describe(
  "getHandBoundingBox",
  () => {

    it(
      "creates a bounding box around hand landmarks",
      () => {

        const landmarks = [
          {
            x: 0.25,
            y: 0.25,
          },

          {
            x: 0.50,
            y: 0.40,
          },

          {
            x: 0.70,
            y: 0.75,
          },
        ];


        const result =
          getHandBoundingBox(
            landmarks,
            640,
            480
          );


        expect(result)
          .not
          .toBeNull();


        expect(result.x)
          .toBeGreaterThanOrEqual(0);


        expect(result.y)
          .toBeGreaterThanOrEqual(0);


        expect(result.width)
          .toBeGreaterThan(0);


        expect(result.height)
          .toBeGreaterThan(0);

      }
    );


    it(
      "returns null when no landmarks exist",
      () => {

        const result =
          getHandBoundingBox(
            [],
            640,
            480
          );


        expect(result)
          .toBeNull();

      }
    );


    it(
      "keeps the bounding box inside the image",
      () => {

        const landmarks = [
          {
            x: 0,
            y: 0,
          },

          {
            x: 0.05,
            y: 0.05,
          },

          {
            x: 0.10,
            y: 0.10,
          },
        ];


        const result =
          getHandBoundingBox(
            landmarks,
            640,
            480
          );


        expect(result.x)
          .toBeGreaterThanOrEqual(0);


        expect(result.y)
          .toBeGreaterThanOrEqual(0);

      }
    );

  }
);