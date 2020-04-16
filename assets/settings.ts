import moment from "moment";

export const config = {};

/* allow configuration from outside */
export function doSettings(
  momentDefaultFormat: string,
  configuration: object
) : void {
  moment.defaultFormat = momentDefaultFormat;
  Object.assign(config, configuration);
};
