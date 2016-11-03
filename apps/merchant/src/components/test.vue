<template>
    <div id="test">
        <h1>I am a title.</h1>
        <a> written by <span v-text='author'></span></a>
    </div>
</template>
<script>
export default {
    data () {
        return {
            author: "微信公众号 jinkey-love"
        }
    }
}
</script>
<style>A
</style>