// Address autocomplete
/* 
    The addressAutocomplete takes as parameters:
  - a container element (div)
  - callback to notify about address selection
  - geocoder options:
     - placeholder - placeholder text for an input element
     - type - location type
     - name - name attribute for an input element
*/
function AutoComplete(container, callback, option) {
	// create label

	var label = document.createElement('label');
	label.innerText = option.label ? option.label : '';
	label.style.color = option.lb_color ? option.lb_color : '#000';
	container.appendChild(label);
	// create an input
	var input = document.createElement('input');
	input.setAttribute('type', 'text');
	if (option.value) {
		input.setAttribute('value', option.value);
	}
	input.setAttribute('placeholder', option.placeholder);
	input.setAttribute('name', option.name);
	input.setAttribute('class', 'form-control');
	input.setAttribute('required', true);
	container.appendChild(input);

	// create a clear button

	var clearButton = document.createElement('div');
	clearButton.classList.add("clear-button");
	addIcon(clearButton);
	clearButton.addEventListener('click', (e) => {
		e.stopPropagation();
		input.value = '';
		callback(null);
		clearButton.classList.remove('visible');
		closeDropDownList();
	});

	var currentPromiseReject;
	input.addEventListener('input', (e) => {

		closeDropDownList();


		var currentValue = this.value;

		// cancel previous request promise
		if (currentPromiseReject) {
			currentPromiseReject({
				canceled: true
			});
		}

		if (!currentValue) {
			clearButton.classList.remove('visible');
			return false;
		}

		var promise = new Promise((resolve, reject) => {
			currentPromiseReject = reject;

			var apiKey = "f510ff426d79491d94496a072fbf8841";
			var url = `https://api.geoapify.com/v1/geocode/autocomplete?text=${encodeURIComponent(currentValue)}&limit=5&apiKey=${apiKey}`;
			console.log(url);
			if (options.type) {
				url += `&type=${option.type}`;
			}

			fetch(url)
				.then(response => {
					// check if it was call successfully
					if (response.ok) {
						response.json().then(data => resolve(data))
					} else {
						response.json().then(data => reject(data))
					}
				});
		});

		clearButton.classList.add('visible');

		promise.then((data) => {
			// Processing the data
			currentItem = data.features;


			// creating a div that will contains items(value)
			var autocompleteItemsElement = document.createElement('div');
			autocompleteItemsElement.setAttribute("class", "autocomplete-items");
			container.appendChild(autocompleteItemsElement)

			// for each item in the result
			data.features?.forEach((element, index) => {
				// div to contain each element
				var itemElement = document.createElement('div');
				// set formated address as value 
				itemElement.innerHTML = features.properties.formated;

				itemElement.addEventListener("click", (e) => {
					input.value = currentItem[index].properties.formated;
					callback(currentItem[index]);
					closeDropDownList();
				})

				autocompleteItemsElement.appendChild(itemElement);


			});
		}, (err) => {
			console.log('eeerrr')
			if (!err.canceled) {
				console.log(err);
			}
		});
	});

	/* Add support for keyboard navigation */
	input.addEventListener("keydown", function (e) {
		var autocompleteItemsElement = container.querySelector(".autocomplete-items");
		if (autocompleteItemsElement) {
			var itemElements = autocompleteItemsElement.getElementsByTagName("div");
			if (e.keyCode == 40) {
				e.preventDefault();
				/*If the arrow DOWN key is pressed, increase the focusedItemIndex variable:*/
				focusedItemIndex = focusedItemIndex !== itemElements.length - 1 ? focusedItemIndex + 1 : 0;
				/*and and make the current item more visible:*/
				setActive(itemElements, focusedItemIndex);
			} else if (e.keyCode == 38) {
				e.preventDefault();

				/*If the arrow UP key is pressed, decrease the focusedItemIndex variable:*/
				focusedItemIndex = focusedItemIndex !== 0 ? focusedItemIndex - 1 : focusedItemIndex = (itemElements.length - 1);
				/*and and make the current item more visible:*/
				setActive(itemElements, focusedItemIndex);
			} else if (e.keyCode == 13) {
				/* If the ENTER key is pressed and value as selected, close the list*/
				e.preventDefault();
				if (focusedItemIndex > -1) {
					closeDropDownList();
				}
			}
		} else {
			if (e.keyCode == 40) {
				/* Open dropdown list again */
				var event = document.createEvent('Event');
				event.initEvent('input', true, true);
				input.dispatchEvent(event);
			}
		}
	});

	function setActive(items, index) {
		if (!items || !items.length) return false;

		for (var i = 0; i < items.length; i++) {
			items[i].classList.remove("autocomplete-active");
		}

		/* Add class "autocomplete-active" to the active element*/
		items[index].classList.add("autocomplete-active");

		// Change input value and notify
		input.value = currentItems[index].properties.formatted;
		callback(currentItems[index]);
	}

	function closeDropDownList() {
		var autocompleteItemsElement = container.querySelector(".autocomplete-items");
		if (autocompleteItemsElement) {
			container.removeChild(autocompleteItemsElement);
		}
	}

	function addIcon(buttonElement) {
		var svgElement = document.createElementNS("http://www.w3.org/2000/svg", 'svg');
		svgElement.setAttribute('viewBox', "0 0 24 24");
		svgElement.setAttribute('height', "24");

		var iconElement = document.createElementNS("http://www.w3.org/2000/svg", 'path');
		iconElement.setAttribute("d", "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z");
		iconElement.setAttribute('fill', 'currentColor');
		svgElement.appendChild(iconElement);
		buttonElement.appendChild(svgElement);
	}

	/* Close the autocomplete dropdown when the document is clicked. 
      Skip, when a user clicks on the input field */
	document.addEventListener("click", function (e) {
		if (e.target !== input) {
			closeDropDownList();
		} else if (!container.querySelector(".autocomplete-items")) {
			// open dropdown list again
			var event = document.createEvent('Event');
			event.initEvent('input', true, true);
			input.dispatchEvent(event);
		}
	});
}
async function getData(text) {
	console.log({
		text
	})
	try {
		url = `http://api.positionstack.com/v1/forward?access_key=${ps_token}&query=${text}&limit=5`;
		let res = await fetch(url);
		return await res.json();
	} catch (error) {

	}
}

function NvAutoComplete(container, option) {

	container.classList.add('autocomplete-wrapper');

	var label = document.createElement('label');
	label.innerText = option.label ? option.label : '';
	label.style.color = option.lb_color ? option.lb_color : '#000';
	container.appendChild(label);
	// create an input
	var input = document.createElement('input');
	input.setAttribute('type', 'text');
	if (option.value) {
		input.setAttribute('value', option.value);
	}
	input.setAttribute('placeholder', option.placeholder);
	input.setAttribute('name', option.name);
	input.setAttribute('class', 'form-control');
	input.setAttribute('required', true);
	container.appendChild(input);

	input.addEventListener('input', async (e) => {
		removeAutoComplete();
		var text = e.target.value;
		text = text.toLowerCase()
		var data;

		if (text.length === 0) {
			removeAutoComplete();
			return;
		}

		data = await getData(text);
		console.log({
			data
		});
		console.log('Data : ', data);
		createAutoComplete(data)

		console.log(data);
	})

	function createAutoComplete(places) {
		var unOrderList = document.createElement('ul');
		unOrderList.classList.add('autocomplete-list');
		unOrderList.id = 'autocomplete-list';
		var list = places['data'];
		console.log({
			list
		});

		list?.map((dt) => {
			var listItem = document.createElement('li');
			var btn = document.createElement('button');
			btn.classList.add('nv-auto-complete-btn');
			btn.innerText = dt['label'];
			btn.addEventListener('click', (e) => {
				e.preventDefault();
				var btn = e.target;
				input.value = btn.innerHTML;
				removeAutoComplete();
			})
			listItem.appendChild(btn);
			unOrderList.appendChild(listItem);
		})
		container.appendChild(unOrderList);

	}

	function removeAutoComplete() {
		const unOrderList = container.querySelector('#autocomplete-list');
		if (unOrderList) {
			unOrderList.remove();
			console.log('remove');
		}
	}

}