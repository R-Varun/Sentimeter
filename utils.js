function validateInput(obj) {
    return new Promise(resolve => {
      valid = true;
      data = obj.data;
      for (var i = 0; i < data.length; i ++) {
        cur = data[i]
        console.log(cur)
        if (typeof cur["speaker"] === "undefined") {
          valid = false;
          break;
        } 
        if (typeof cur["utterance"] === "undefined") {
          valid = false;
          break;
        } 
      }
      resolve(valid);
    })
}



module.exports = {
    validateInput
}



