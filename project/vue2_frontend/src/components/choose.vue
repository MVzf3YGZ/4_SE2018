<template>
  <div>
    <div style="width:100%">
      <div id="choose1" style="  float:left">
        <img src="../assets/img/1.png" @click="jump1">
      </div>
      <div id="choose2" style="float:left ">
        <img src="../assets/img/2.png" @click="jump2">
      </div>
    </div>
    <div style="width:100%">
      <div id="choose3" style="float:left ">
        <img src="../assets/img/3.png" @click="jump3">
      </div>
      <div id="choose4" style="float:left ">
        <img src="../assets/img/4.png" @click="jump4">
      </div>

    </div>

  </div>
</template>
<script>
  export default {
    name: "choose",
    methods: {
      jump1() {
        this.$router.replace('/echart1')
      },
      jump2() {
        this.$router.replace('/echart2')
      },
      jump3() {
        this.$router.replace('/echart3')
      },
      jump4() {
        this.$router.replace('/echart4')
      },
    }
  }
</script>
