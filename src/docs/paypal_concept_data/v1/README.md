# React Testing

```javascript
// HelloWorld.js a react component

import React from 'react';

const HelloWorld = () =>{
    return(
    	<div data-testid='test-id-1'>
        Hello World
        </div>
    )
}
```

the html element should contain an attribute called `data-testid` , we will use this test id as reference to individual react components while performing UI tests

make a new directory called __\_\test__  __ 

```javascript
// ComponentName.test.js 

import { render,screen,cleanup } from '@testing-library/react';

import renderer from 'react-test-renderer';

import ComponentName from './path/to/file/ComponentName.js';

// after each test cleanup console
afterEach(()=>{
    cleanup();
});

test('purpose of this test',()=>{
    
    render(<ComponentName />);
    
    const componentNameElement = screen.getByTestId('test-id-name');
    
    expect(componentNameElement).toBeInTheDocument();
    
    expect(componentNameElement).toHaveTextContent("Some Text Content as STRING");
})

test('purpose of this (another/second) test',()=>{
    
    const samplePropData = {
        key1 : value1,
        key2 : value2,
        key3 : value3
    };
    
    render(<ComponentName propName={samplePropData}/>);
    
    const componentNameElement = screen.getByTestId('test-id-name');
    
    expect(componentNameElement).toBeInTheDocument();
    
	// here in this test case
	// expect(componentNameElement).toHaveTextContent("Some Text Content as STRING");
	// must contain a text that is assigned as
	// one of the values of any of the keys in samplePropData
    expect(componentNameElement).toHaveTextContent("Some Text Content as STRING");
	// to obtain an all tests passed

	expect(componentNameElement).toContainHTML('<someHTMLelement>');

	expect(componentNameElement).not.toContainHTML('<someHTMLelement>');
})


// OPTIONAL __SNAPSHOT__ TESTS
test('some snapshot test for example- current UI state matches snapshot', ()=>{
    const samplePropData = {
        key1 : value1,
        key2 : value2,
        key3 : value3
    };
    
	const tree = renderer.create(<ComponentName propName={samplePropData}/>).toJSON();
     
    expect(tree).toMatchSnapshot();
})
```



---

original test script for **LinkinDemo**

```json
"test": "jest --coverage ./__tests__/"
```

**LinkinDemo** is based on next js

