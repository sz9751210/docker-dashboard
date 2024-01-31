<template>
  <div>
    <el-button type="primary" @click="fetchDockerImages"
      >List Docker Images</el-button
    >
    <el-table :data="dockerImagesParsed" style="width: 100%">
      <el-table-column prop="repository" label="REPOSITORY"></el-table-column>
      <el-table-column prop="tag" label="TAG"></el-table-column>
      <el-table-column prop="imageId" label="IMAGE ID"></el-table-column>
      <el-table-column prop="created" label="CREATED"></el-table-column>
      <el-table-column prop="size" label="SIZE"></el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      dockerImages: "",
      dockerImagesParsed: [],
    };
  },
  methods: {
    fetchDockerImages() {
      axios
        .get("http://127.0.0.1:5000/list-docker-images")
        .then((response) => {
          this.dockerImages = response.data.images;
          this.parseDockerImages();
        })
        .catch((error) => console.error("Error:", error));
    },
    parseDockerImages() {
      const lines = this.dockerImages.split("\n").slice(1); // Remove the header line
      this.dockerImagesParsed = lines.map((line) => {
        const parts = line.split(/\s{2,}/); // Split by two or more spaces
        return {
          repository: parts[0],
          tag: parts[1],
          imageId: parts[2],
          created: parts[3],
          size: parts[4],
        };
      });
    },
  },
};
</script>
