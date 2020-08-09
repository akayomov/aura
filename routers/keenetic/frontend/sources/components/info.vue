<template>
	<div class="info" :class="(status?'status-'+status:'')+(status&&design?' ':'')+(design?'design-'+design:'')">
		<i v-if="icon!==''" :class="'gg-'+icon"/>
		<span v-if="text!==''" :class="{'with-icon': icon!==''}">{{currentText}}</span>
	</div>
</template>

<script lang="ts">
import {Vue, Component, Prop, Watch} from 'vue-property-decorator'

@Component
export default class Info extends Vue {
	@Prop({default:""}) readonly icon!: string;
	@Prop({default:""}) readonly text!: string;
	@Prop({default:""}) readonly status!: string;
	@Prop({default:""}) readonly design!: string;

	currentText: string = this.text

	@Watch('text')
	onTextUpdate(val: string) { this.currentText = val }
}
</script>

<style scoped lang="less">
@import "../tools/colors";

.info {
	font-family: 'default', serif;
	display: flex;
	flex-direction: row;
	align-items: center;
	padding: 2px;

	width: fit-content;

	span {
		user-select: none;
		&.with-icon { margin-left: 5px; }
	}

	&.status-red { i, span{ color: @info-text-red; font-weight: bold } }
	&.status-yellow { i, span{ color: @info-text-yellow; font-weight: bold } }
	&.status-green { i, span{ color: @info-text-green; font-weight: bold } }
}
</style>