<template>
  <div
    class="component_inputs"
    v-for="(param, index) in server_parameters"
    :key="index"
  >
    <label class="padding_for_input" :for="param.name">{{ param.name }}</label>
    <InputText
      v-if="param.type === 0"
      :placeholder="param.name"
      v-model="parsed_param_values[index]"
      @input="data_validation"
    />
    <InputNumber
      v-else-if="param.type === 1"
      :placeholder="param.name"
      v-model="parsed_param_values[index]"
      @input="data_validation"
    />
    <DatePicker
      v-else-if="param.type === 2"
      :placeholder="param.name"
      v-model="parsed_param_values[index]"
      :manualInput="false"
      dateFormat="dd/mm/yy"
      @update:modelValue="data_validation"
    />
    <DatePicker
      v-else-if="param.type === 3"
      :placeholder="param.name"
      v-model="parsed_param_values[index]"
      showTime
      hourFormat="24"
      fluid
      :manualInput="false"
      dateFormat="dd/mm/yy "
      @update:modelValue="data_validation"
    />
    <Checkbox
      v-else-if="param.type === 4"
      v-model="parsed_param_values[index]"
      binary
      @change="data_validation"
    />
    <Select
      v-else-if="param.type === 5"
      v-model="parsed_param_values[index]"
      :options="param.available_values"
      @change="data_validation"
    />
  </div>
</template>
<script>
import InputText from "primevue/inputtext";
import InputNumber from "primevue/inputnumber";
import DatePicker from "primevue/datepicker";
import Checkbox from "primevue/checkbox";
import Select from "primevue/select";
import { parameterType } from "../DisplayedDashboard/displayed-dashboard";
export default {
  name: "ServerParameters",
  props: ["server_parameters"],
  data() {
    return {
      parsed_param_values: [],
    };
  },
  methods: {
    data_validation() {
      let updated_values = {};
      for (var i = 0; i < this.server_parameters.length; i++) {
        updated_values[this.server_parameters[i].name] =
          this.parsed_param_values[i];
      }
      this.$emit("update:server_parameters", updated_values);
    },
  },
  beforeMount() {
    for (var i = 0; i < this.server_parameters.length; i++) {
      let value = this.server_parameters[i].value
        ? this.server_parameters[i].value
        : this.server_parameters[i].default;
      switch (this.server_parameters[i].type) {
        case parameterType.string:
          this.parsed_param_values.push(
            typeof value === "string" ? value : value.toString(),
          );
          break;
        case parameterType.number:
          this.parsed_param_values.push(
            typeof value === "number" ? value : parseFloat(value),
          );
          break;
        case parameterType.date:
          this.parsed_param_values.push(new Date(value));
          break;
        case parameterType.datetime:
          this.parsed_param_values.push(new Date(value));
          break;
        case parameterType.boolean:
          this.parsed_param_values.push(
            typeof value === "boolean"
              ? value
              : value === "true"
                ? true
                : false,
          );
          break;
        case parameterType.select:
          this.parsed_param_values.push(value);
          break;
      }
    }
  },
  components: {
    InputText,
    InputNumber,
    DatePicker,
    Checkbox,
    Select,
  },
};
</script>
