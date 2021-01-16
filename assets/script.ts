import conf from "./settings";
import { colorizeSO } from "./colors";
import { drawCharts } from "./charts";
import { dropToggle } from "./dropdowns";
import { flashClose } from "./notifications";
import { momentTime } from "./moments";
import { sApiHelper } from "./space";

conf.initialize();

colorizeSO();
drawCharts();
dropToggle();
flashClose();
momentTime();
sApiHelper();
