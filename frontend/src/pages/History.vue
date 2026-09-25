<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const openId = ref(null)
const detail = ref(null)
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
const isBatch = r => Array.isArray(r.result?.rooms)
const roomCell = r => isBatch(r) ? `合并 ${r.result.rooms.length} 房` : r.room_name
const countCell = r => isBatch(r) ? r.result.total?.order_count : r.result?.order_count
async function toggle(id) {
  if (openId.value === id) { openId.value = null; detail.value = null; return }
  openId.value = id
  detail.value = await getJSON(`/api/runs/${id}`)
}
</script>
<template>
  <div class="page">
    <h1>测算记录</h1>
    <table class="tbl">
      <thead><tr><th>时间</th><th>房间</th><th>砖型</th><th>片数</th><th></th></tr></thead>
      <tbody>
        <template v-for="r in items" :key="r.id">
          <tr class="run-row">
            <td>{{ r.created_at?.slice(0, 19) }}</td>
            <td>{{ roomCell(r) }}</td>
            <td>{{ r.tile_name }}</td>
            <td>{{ countCell(r) }}</td>
            <td><button class="link-btn" @click="toggle(r.id)">{{ openId === r.id ? '收起' : '详情' }}</button></td>
          </tr>
          <tr v-if="openId === r.id && detail" class="run-detail">
            <td colspan="5">
              <table v-if="isBatch(detail)" class="tbl">
                <thead><tr><th>房间</th><th>尺寸 m</th><th>净用量</th><th>下单片数</th></tr></thead>
                <tbody>
                  <tr v-for="room in detail.result.rooms" :key="room.room_id">
                    <td>{{ room.room_name }}</td>
                    <td>{{ room.length }}×{{ room.width }}</td>
                    <td>{{ room.raw_count }}</td>
                    <td>{{ room.order_count }}</td>
                  </tr>
                  <tr>
                    <td><strong>合计</strong></td>
                    <td>—</td>
                    <td><strong>{{ detail.result.total.raw_count }}</strong></td>
                    <td><strong>{{ detail.result.total.order_count }}</strong></td>
                  </tr>
                </tbody>
              </table>
              <p v-else>净用量 {{ detail.result?.raw_count }} 片，损耗 {{ detail.result?.waste_pct }}%</p>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>
