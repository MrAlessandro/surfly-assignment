<template>
  <div class="user-form">
    <h1>Enter Your Username</h1>
    <form @submit.prevent="submitUsername">
      <input
        v-model="username"
        type="text"
        placeholder="Enter username"
        required />
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "../stores/userStore"; // Adjust the path as needed

const userStore = useUserStore();
const username = ref(userStore.username);
const router = useRouter();

const submitUsername = () => {
  if (username.value.trim()) {
    userStore.setUsername(username.value);
    router.push("/drawer"); // Redirect to the canvas page
  }
};
</script>

<style scoped>
.user-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}
input {
  margin-bottom: 10px;
  padding: 5px;
}
button {
  padding: 5px 10px;
}
</style>
