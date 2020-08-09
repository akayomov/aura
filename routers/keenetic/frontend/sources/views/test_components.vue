<template>
	<div class="test-components-view">
		<div class="infos">
			<h1>INFOS</h1>
			<info text="Text only"/>
			<info text="Text only green status" status="green"/>
			<info text="Text only yellow status" status="yellow"/>
			<info text="Text only red status" status="red"/>
			<div class="row">
				<info icon="arrange-back"/>
				<info icon="arrange-back" status="red"/>
				<info icon="arrange-back" status="yellow"/>
				<info icon="arrange-back" status="green"/>
			</div>
			<info text="Copyright (AURA)" icon="copyright"/>
		</div>
		<div class="knobs">
			<h1>KNOBS</h1>
			<div class="row">
				<knob>Button</knob>
				<knob><info text="Infoed button"/></knob>
				<knob><info text="Fully informative button" icon="arrange-back" status="yellow"/></knob>
			</div>
			<knob type="switch">Simple switch</knob>
			<knob type="switch"><info text="Switcher with label" icon="arrange-back"/></knob>
			<knob type="switch" initial-status="true"><info text="Is on by default" icon="arrange-back" status="green"/></knob>
			<knob type="checkbox">Checkbox label</knob>
			<div class="row">
				<knob type="switch" />
				<knob type="checkbox" />
			</div>
		</div>
		<div class="fields">
			<h1>FIELDS</h1>
			<field placeholder="Testing" icon="copyright" editing="false"/>
			<div class="row">
				<knob type="switch" @update="handleEdit" :status="editHandler"/>
				<field placeholder="" :editing="editHandler"/>
			</div>
			<info icon="arrange-back" text="Identity"/>
			<field icon="arrange-back" value="Identity" editing="false"/>
		</div>
	</div>
</template>

<script lang="ts">
import {Vue, Component} from 'vue-property-decorator';
import knob from '../components/knob.vue';
import info from "../components/info.vue";
import field from "../components/field.vue";

@Component({components:{knob, info, field}})
export default class TestComponents extends Vue {

	editHandler: boolean = true;
	handleEdit(val:boolean) { this.editHandler = val }
}
</script>

<style scoped lang="less">
.test-components-view {
	display: flex;
	flex-direction: column;
	flex-grow: 1;

	.row {
		display: flex;
		flex-direction: row;

		button {
			margin-right: 5px;
			&:last-child {
				margin-right: 0px;
			}
		}
	}

}

</style>