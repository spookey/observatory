import axios from "axios";
import Chart from "chart.js";
import { colorizeSO } from "./colors";
import { colorizeTX } from "./colors";
import { flashClose } from "./notifications";
import { momentTime } from "./moments";

colorizeSO();
colorizeTX();
flashClose();
momentTime();
