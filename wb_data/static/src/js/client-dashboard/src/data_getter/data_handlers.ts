import { ChartComponent } from "../components/DisplayedDashboard/displayed-dashboard";
export class DataHandler {
  component: ChartComponent;
  parameters: any;
  constructor(component: ChartComponent, parameters: any) {
    this.component = component;
    this.parameters = parameters;
  }

  getParameters() {
    return this.parameters;
  }

  setParameters(parameters: any) {
    this.parameters = parameters;
  }

  getParameterByName(name: string) {
    return this.getParameters()[name];
  }

  setParameterByName(name: string, value: any) {
    let parameters = this.getParameters();
    parameters[name] = value;
    this.setParameters(parameters);
  }

  interpretDefaults(parameters) {
    let updated_values = {};
    for (var i = 0; i < parameters.length; i++) {
      updated_values[parameters[i].name] = parameters[i].default_value;
    }
    return updated_values;
  }
}
