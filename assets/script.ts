import { conf } from "./settings";

import { colorizeSO } from "./colors";
import { drawCharts } from "./charts";
import { flashClose } from "./notifications";
import { momentTime } from "./moments";


(window as any).configure = conf.configure;

colorizeSO();
drawCharts();
flashClose();
momentTime();
