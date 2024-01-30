<template>
  <div>
    <input type="text" v-model="folderPath" placeholder="Enter folder path" />
    <button @click="runDockerCompose">Run Docker Compose</button>
    <div v-if="output">
      <h3>Output:</h3>
      <pre>{{ output }}</pre>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "DockerComposeRunner",
  data() {
    return {
      folderPath: "",
      output: "",
    };
  },
  methods: {
    async runDockerCompose() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/run-docker-compose",
          { folderPath: this.folderPath }
        );
        this.output = response.data;
      } catch (error) {
        console.error(error);
        this.output = "Error: " + error.message;
      }
    },
  },
};
</script>
