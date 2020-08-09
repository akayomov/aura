<template>
	<div class="dashboard">
		<h1>Dashboard</h1>

		<p>{{stateTesting}}</p>
		<knob @click="outerHandler">
			<knob @click="innerHandler">
				<i class="gg-copyright" /><div>Some text</div>
			</knob>
		</knob>
	</div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { State, Getter, Action, Mutation } from 'vuex-class'
import knob from '../components/knob.vue'

@Component({components: {knob}})
export default class Dashboard extends Vue {
	@State testing: string

	stateTesting: string = this.testing;

	outerHandler() {
		console.log('outer')
	}

	innerHandler() {
		console.log('inner')
	}

	created () {
		this.stateTesting = this.testing;
	}
}
</script>

<style scoped lang="less">
div.dashboard {
	.gg-copyright {
		--ggs: 1; // x 18px
	}

	display: flex;
	flex-direction: column;
	flex-grow: 1;
	align-items: center;
}
</style>