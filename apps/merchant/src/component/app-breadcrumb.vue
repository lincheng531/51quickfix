<template>
    <div class="p-t-sm">
        <ol class="breadcrumb">
            <li v-for="item in breadcrumb">
                <a class="text-muted"><span v-text="item.title"></span></a>
            </li>
        </ol>
    </div>
</template>

<script>
    export default {
        props: ['breadcrumb'],
    }
</script>

<style>
    .breadcrumb {
        margin-bottom: 0;
        background: transparent;
    }
</style>