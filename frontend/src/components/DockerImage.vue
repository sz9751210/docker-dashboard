<template>
  <div>
    <div class="sidebar">
      <el-button type="primary" @click="fetchDockerImages"
        >List Docker Images</el-button
      >
    </div>
    <div class="content">
      <el-table
        v-if="dockerImagesParsed.length > 0"
        :data="dockerImagesParsed"
        style="width: 100%"
      >
        <el-table-column prop="repository" label="REPOSITORY"></el-table-column>
        <el-table-column prop="tag" label="TAG"></el-table-column>
        <el-table-column prop="imageId" label="IMAGE ID"></el-table-column>
        <el-table-column prop="created" label="CREATED"></el-table-column>
        <el-table-column prop="size" label="SIZE"></el-table-column>
        <el-table-column label="ACTION">
          <template v-slot="scope">
            <el-button size="mini" @click="openStartDialog(scope.row)"
              >Start</el-button
            >
          </template>
        </el-table-column>
      </el-table>

      <el-dialog title="Start Container" v-model="startDialogVisible">
        <el-form :model="startForm">
          <el-form-item label="Container Name">
            <el-input v-model="startForm.containerName"></el-input>
          </el-form-item>

          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="Host Port">
                <el-input v-model="startForm.hostPort"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="Container Port">
                <el-input v-model="startForm.containerPort"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <template v-slot:footer>
          <el-button @click="startDialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="startContainer">Confirm</el-button>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  components: {},
  data() {
    return {
      dockerImages: "",
      dockerImagesParsed: [],
      startDialogVisible: false,
      selectedImage: null,
      isSidebarCollapsed: false,
      startForm: {
        containerName: "",
        hostPort: "",
        containerPort: "",
      },
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
    openStartDialog(row) {
      this.selectedImage = row.repository;
      this.startDialogVisible = true;
    },
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
    },
    startContainer() {
      axios
        .post("http://127.0.0.1:5000/start-container", {
          repository: this.selectedImage,
          containerName: this.startForm.containerName,
          hostPort: this.startForm.hostPort,
          containerPort: this.startForm.containerPort,
          // 添加其他字段
        })
        .then((response) => {
          console.log(response.data);
          // 處理響應
        })
        .catch((error) => {
          console.error("Error:", error);
        });

      this.startDialogVisible = false;
    },
  },
};
</script>
<style scoped>
.app-container {
  display: flex;
}

.sidebar {
  width: 200px;
  transition: width 0.3s ease;
  /* your existing styles */
}

.content {
  flex-grow: 1;
}
</style>
