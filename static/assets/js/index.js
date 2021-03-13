
;
 (function (root, factory) {
	if (typeof exports === "object") {
		// CommonJS
		module.exports = exports = factory();
	}
	else if (typeof define === "function" && define.amd) {
		// AMD
		define([], factory);
	}
	else {
		// Global (browser)
		root.GaugeMeter = factory();
	}
} (this, function () {
	var GaugeMeter = function GaugeMeter(element, opts) {
		if (!element) {
			throw new Error("No element provided!");
		}
		var val = 90;
		var colorr= '#F00000'
		if (val>0 && val <50){
			colorr = '#00FF00'
		}
		else if (val>50 && val <100) {
			colorr = '#FF0000'
		}
		this.element = element;
		this.options = {
			color: colorr,
			lineWidth: 20,
			animation: true,
			innerGauge: true,
			innerGaugeColor: '#999999'
		};
		opts = opts || {};
		var that = this;
		Object.keys(opts).forEach(function (key) {
			that.options[key] = opts[key];
		});
		this.prepareElement();
		return this;
	};

	/*=====================================================
	 *	_ Prototype Functions
	 ============================*/
	GaugeMeter.prototype = {
		/*=====================================================
		 *	Prepeare Element : Draw the Gauge for the provided input options
		=============================*/
		prepareElement: function () {
			var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
			svg.setAttribute('width', this.element.offsetWidth);
			svg.setAttribute('height', this.element.offsetHeight);
			svg.setAttribute('viewBox', '0 0 400 400')
			this.svg = svg;

			var outerPath = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
			outerPath.setAttribute('r', 175);
			outerPath.setAttribute('cx', 200);
			outerPath.setAttribute('cy', 300);
			outerPath.setAttribute('stroke', '#EEEEEE');
			outerPath.setAttribute('stroke-width', '50');
			outerPath.setAttribute('fill', 'transparent');

			var outerGauge = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
			outerGauge.setAttribute('r', 175);
			outerGauge.setAttribute('cx', 200);
			outerGauge.setAttribute('cy', 300);
			outerGauge.setAttribute('stroke', this.options.color);
			outerGauge.setAttribute('stroke-width', '50');
			outerGauge.setAttribute('fill', 'transparent');
			outerGauge.setAttribute('stroke-dasharray', '0, 1000000');
			outerGauge.setAttribute('transform', 'rotate(-220 200 300)');
			this.outerGauge = outerGauge;

			var innerGauge = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
			innerGauge.setAttribute('r', 145);
			innerGauge.setAttribute('cx', 200);
			innerGauge.setAttribute('cy', 300);
			innerGauge.setAttribute('stroke', this.options.innerGaugeColor);
			innerGauge.setAttribute('stroke-width', '11');
			innerGauge.setAttribute('fill', 'transparent');
			innerGauge.setAttribute('stroke-dasharray', '0, 1000000');
			innerGauge.setAttribute('transform', 'rotate(-225 200 300)');
			this.innerGauge = innerGauge;

			// var label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
			// label.setAttribute('x', '200');
			// label.setAttribute('y', '80');
			// label.setAttribute('fill', '#CCCCCC');
			// label.setAttribute('font-size', '25px');
			// label.setAttribute('font-family', 'Arial');
			// label.setAttribute('text-anchor', 'middle');
			// label.innerHTML = '100%';

			// var line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
			// line.setAttribute('x1', '200');
			// line.setAttribute('y1', '90');
			// line.setAttribute('x2', '200');
			// line.setAttribute('y2', '170');
			// line.setAttribute('stroke', '#000000');
			// line.setAttribute('stroke-width', '1');
			// line.setAttribute('stroke-dasharray', '2, 1');

			var gaugeLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
			gaugeLabel.setAttribute('x', '200');
			gaugeLabel.setAttribute('y', '350');
			gaugeLabel.setAttribute('fill', '#999999');
			gaugeLabel.setAttribute('font-size', '75px');
			gaugeLabel.setAttribute('font-family', 'Arial');
			gaugeLabel.setAttribute('font-weight', 'bold');
			gaugeLabel.setAttribute('text-anchor', 'middle');
			this.gaugeLabel = gaugeLabel;

			svg.appendChild(outerPath);
			svg.appendChild(outerGauge);
			svg.appendChild(innerGauge);
			// svg.appendChild(label);
			// svg.appendChild(line);
			svg.appendChild(gaugeLabel);
			this.element.appendChild(svg);
		},
		/*=====================================================
		 *	Set Value : Set the Value for the Guage Meter
		=============================*/
		setValue: function (value,max,speed) {
			console.log(value)
			if (value == undefined) {
				throw new Error("Provide a value to be set for Gauge meter!");
			}
			this.value = value;
			var _this = this;
			function drawValue(drawnValue) {
				_this.outerGauge.setAttribute('stroke-dasharray', (drawnValue * max) + ', 1000000');
				_this.gaugeLabel.innerHTML = drawnValue ;
				if (drawnValue < _this.value) {
					drawnValue = drawnValue + 1;
					setTimeout(function () {
						drawValue(drawnValue);
					}, speed);
				}
			}
			if (this.options.animation) {
				drawValue(0);
			} else {
				drawValue(this.innerValue);
			}
		},
		/*=====================================================
		 *	Set Inner Ring Value : Set the Value for the Inner Ring in Guage Meter
		=============================*/
		setInnerValue: function (value,max,speed) {
			if (!this.options.innerGauge) {
				throw new Error("Inner Gauge is not Available!");
			}
			if (value == undefined) {
				throw new Error("Please provide value for Inner Gauge!");
			}
			this.innerValue = value;
			var _this = this;
			function drawValue(drawnValue) {
				_this.innerGauge.setAttribute('stroke-dasharray', (drawnValue * (max-0.2)) + ', 1000000');
				if (drawnValue < _this.innerValue) {
					drawnValue = drawnValue + 1;
					setTimeout(function () {
						drawValue(drawnValue);
					}, speed);
				}
			}
			if (this.options.animation) {
				drawValue(0);
			} else {
				drawValue(this.innerValue);
			}
		}
	};
	return GaugeMeter;
}));

