<template>
  <div class="app-container">
    <!-- Container -->
    <el-container>
      <!-- Sidebar -->
      <el-aside :width="isSidebarCollapsed ? '0px' : '200px'" class="sidebar">
        <div
          class="sidebar-content"
          :style="{ 'margin-top': isSidebarCollapsed ? '10px' : '60px' }"
        >
          <el-button type="primary" @click="fetchDockerImages"
            >List Docker Images</el-button
          >
          <el-button type="primary" @click="fetchDockerContainers"
            >List Docker Containers</el-button
          >
        </div>
      </el-aside>

      <!-- Main Content -->
      <el-main class="main-content">
        <!-- Collapse Button -->
        <el-button
          type="primary"
          icon="el-icon-menu"
          @click="toggleSidebar"
          class="collapse-btn"
        >
          <img :src="require('@/assets/collapseleft.png')" alt="Button Image" />
        </el-button>

        <!-- Content Here -->
        <div class="content">
          <el-table
            v-if="dockerImagesParsed.length > 0"
            :data="dockerImagesParsed"
            style="width: 100%"
          >
            <el-table-column
              prop="repository"
              label="REPOSITORY"
            ></el-table-column>
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
          <!-- 新增展示容器的表格 -->
          <el-table
            v-if="dockerContainersParsed.length > 0"
            :data="dockerContainersParsed"
            style="width: 100%"
          >
            <el-table-column
              prop="containerId"
              label="CONTAINER ID"
            ></el-table-column>
            <el-table-column prop="imageName" label="IMAGE"></el-table-column>
            <el-table-column prop="command" label="COMMAND"></el-table-column>
            <el-table-column prop="created" label="CREATED"></el-table-column>
            <el-table-column prop="status" label="STATUS"></el-table-column>
            <el-table-column prop="ports" label="PORTS"></el-table-column>
            <!-- 其他需要的列 -->
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
              <el-button type="primary" @click="startContainer"
                >Confirm</el-button
              >
            </template>
          </el-dialog>
        </div>
      </el-main>
    </el-container>
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
      dockerContainers: "",
      dockerContainersParsed: [],
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
    fetchDockerContainers() {
      axios
        .get("http://127.0.0.1:5000/list-docker-containers")
        .then((response) => {
          this.dockerContainers = response.data.containers;
          this.parseDockerContainers();
        })
        .catch((error) => console.error("Error:", error));
    },
    parseDockerContainers() {
      const lines = this.dockerContainers.split("\n").slice(1); // 移除標頭行
      this.dockerContainersParsed = lines.map((line) => {
        const parts = line.split(/\s{2,}/); // 用兩個或更多空格分割
        return {
          containerId: parts[0],
          imageName: parts[1],
          command: parts[2],
          created: parts[3],
          status: parts[4],
          ports: parts[5],
          name: parts[6],
          // 根據您的容器資訊格式，這裡可能需要添加或移除某些字段
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
  font-family: "Segoe UI", Arial, sans-serif;
  color: #fff;
}

.sidebar {
  background-color: #b3d4fc; /* 淺藍色 */
  transition: width 0.3s;
  border-right: 1px solid #d3e0ea;
}

.main-content {
  background-color: #1e3d59; /* 深藍色 */
  padding-top: 70px;
  /* padding: 50px; */
}

.collapse-btn {
  display: flex; /* 使用 flex 布局 */
  justify-content: center; /* 保证内容居中 */
  align-items: center; /* 垂直居中 */
  left: 0;
  top: 10px;
  z-index: 1000;
  transition: left 0.3s;
  color: #1e3d59; /* 按鈕顏色 */
  border-color: #1e3d59;
}

.collapse-btn img {
  width: 30px; /* 或者您希望的尺寸 */
  height: auto;
  margin-right: 5px;
  order: -1;
}

.el-main {
  position: relative;
}

.sidebar-content {
  transition: margin-top 0.3s;
  padding: 20px;
}

.el-button {
  margin: 10px 0;
  border: none;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.el-button-primary {
  background-color: #1e3d59;
  border-color: #1e3d59;
}
</style>
