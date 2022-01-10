class ColorPaletteGenerator{
    //https://sashamaps.net/docs/resources/20-colors/
    static predefinedColors =[
        "#e6194B",
        "#3cb44b",
        "#ffe119",
        "#4363d8",
        "#f58231",
        "#911eb4",
        "#42d4f4",
        "#f032e6",
        "#bfef45",
        "#fabed4",
        "#469990",
        "#9A6324",
        "#800000",
        "#808000",
        "#000075",
        "#a9a9a9",
        "#000000",
    ]
    static GetColorPalette(number_of_colors){
        let ret = {};
        for(let i = 0; i < number_of_colors; i++)
        {
            if(i < this.predefinedColors.length)
                ret[i] = this.predefinedColors[i]
            else
                //https://css-tricks.com/snippets/javascript/random-hex-color/
                ret[i] = "#"+Math.floor(Math.random()*16777215).toString(16);
        }
        return ret;
    }
}

export default ColorPaletteGenerator