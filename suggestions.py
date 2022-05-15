class Suggestions():
    @staticmethod
    def cardboard():
        text = [
            'Reuse by offering to friends/colleagues who might be moving house',
            'Recycle in your recycling bin or drop it off at your local Recycling and Waste Centre',
            'Recycle by tearing into small pieces and adding to your home compost bin'
        ]
        link = 'https://recyclingnearyou.com.au/paper-cardboard/boroondaravic'

        return (text, link)

    @staticmethod
    def ewaste():
        text = [
            'The Victorian Government has banned all e-waste from going to landfill. You must not put any e-waste in any of your bins.',
            'Before recycling your e-waste, consider donating or selling it first. This is always better than recycling.',
            'Please drop off this item at your local Recycling and Waste Centre',
        ]
        link = 'https://www.boroondara.vic.gov.au/waste-environment/recycling-and-waste/e-waste-electronic-waste'

        return (text, link)

    @staticmethod
    def glass():
        text = [
            'If your glass is not a bottle or jar, please dispose of in your household waste bin. You can also drop it off at your local Recycling and Waste Centre',
            'For glass bottles and jars, you can try reusing them as water bottles or vases or for storing food and small items',
            'Please recycle glass bottles and jars in your recyling bin or at your local Recycling and Waste Centre',
        ]
        link = 'https://www.gpi.org/glass-recycling-facts'

        return (text, link)

    @staticmethod
    def metal():
        text = [
            'Recycle in your recycling bin or drop off at your local Recycling and Waste Centre'
        ]
        link = 'https://recyclingnearyou.com.au/scrap-metals/BoroondaraVIC'

        return (text, link)

    @staticmethod
    def paper():
        text = [
            'Recycle in your recycling bin or drop off at your local Recycling and Waste Centre'
        ]
        link = 'https://recyclingnearyou.com.au/paper-cardboard/'

        return (text, link)

    @staticmethod
    def plastic():
        text = [
            'If your plastic is a bottle or rigid container, recycle in your recycling bin or drop off at your local Recycling and Waste Centre',
            'If it is a type of soft plastic, recycle it are your local Coles or Woolsworths via the REDcycle flexibile/soft plastics recycling program'
        ]
        link = 'https://recyclingnearyou.com.au/plastic/'

        return (text, link)

    @staticmethod
    def trash():
        text = [
            'Dispose of this item using your household waste bin or drop off at your local Recycling and Waste Centre'
        ]
        link = 'https://www.boroondara.vic.gov.au/waste-environment/recycling-and-waste/boroondara-recycling-and-waste-centre'

        return (text, link)
