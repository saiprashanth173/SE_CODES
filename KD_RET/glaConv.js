

var convert= ["convert","conv","meters","m","centimeter","picometer","millimeter","mm","cm","pm","nanometer","nm","yard","mile","inch","foot","ft","m2","cm2","meter-square","square-meter","square-centimeter","centimeter-square","cm-square","m-square","m-sq","cm-sq","sq-m","sq-cm","min","sec","ms","minutes","seconds","milliseconds","farenheit","kelvin","celcius","c","f","k"];
var length= ["meters","m","centimeter","picometer","millimeter","mm","cm","pm","nanometer","nm","yard","mile","inch","foot","ft"];
var area = ["m2","cm2","meter-square","square-meter","square-centimeter","centimeter-square","cm-square","m-square","m-sq","cm-sq","sq-m","sq-cm"];
var time = ["min","sec","ms","minutes","seconds","milliseconds"];
var mass = ["kg","kilogram","ton","gram","ounce","milligram","mg","pound"];
var temperature = ["farenheit","kelvin","celcius","c","f","k"];
var getType = {4:"length",9:"area",16:"time",25:"mass",36:"temperature"};
var modules = [length,area,time,mass,temperature];


function getWords(query){

query=query.toLowerCase();
subQuery = query.replace(/\d+/g,"");

var splitString = subQuery.split(" ");
var flag=0;
var digit = 1;
var determine =1;
var finalReturn = {};

for (i=0;i<=splitString.length;i++)
{

	if (convert.indexOf(splitString[i])>=0)
	{

		flag+=1;
		if (flag==2)
		{
		break;
		}
	}
}

if (flag == 2){
	var storeLis =[];
	
	var pattern =/convert (\d+)\s?(.*) to (.*)|(\d+)\s?(.*) to (.*)|convert (.*) to (.*)|from (.*) to (.*)|(.*) to (.*)|(\d+)\s?(.*) to (.*)|(.*) - (.*)/i;
	
	var val = query.match(pattern);
	console.log(query);
	if (val!=null)
	{
	for (i=0;i<val.length;i++)
	{
		if (! (typeof val[i] == "undefined"))
		{	
			if(val[i].trim().indexOf(" ")<0)
			{
			storeLis.push(val[i]);			
			}
		}
	}

	for(j=0;j<modules.length;j++)
		{
			for (i=0;i<splitString.length;i++)
			{

				if (modules[j].indexOf(splitString[i])>=0) 
				{
					console.log(splitString[i]);
					determine = determine*(j+2);
				}
			}
		}

		if (Object.keys(getType).indexOf(""+determine)>=0)
		{
		if (storeLis.length==2)
		{
			finalReturn = {"type":getType[determine],"value":digit,"from":storeLis[0],"to":storeLis[1]};
		}

		else if(storeLis.length==3)
		{

			if (parseInt(storeLis[0]) != "NaN")
				digit=parseInt(storeLis[0]);

			finalReturn = {"type":getType[determine],"value":digit,"from":storeLis[1],"to":storeLis[2]};			

		}
		}
	}

console.log(finalReturn);
return finalReturn;
}
}

getWords("convert 10 m to cm");