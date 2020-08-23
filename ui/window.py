
import pygame
import time

from ui.event import EventBox
from ui import colors
from ui import textwrap
from ui.factory import FactoryBox
from ui.offbooks import OffBooksProducerBox

class Window:
    def __init__(self, screen, width, height, fontsizes):
        self.screen = screen
        self.width = width
        self.height = height

        self.game_data = None

        self.event_list = []
        self.event_height = height // 11
        self.event_width = width // 5
        self.event_font = pygame.font.Font(
            'freesansbold.ttf',
            fontsizes["events"]
        )
        self.event_surface = pygame.Surface((self.event_width, height))
        self.event_surface_pos = (width-self.event_width, 0)
        self.event_xpos = self.event_surface_pos[0]
        self.oldest_event = None

        # width of left part of screen
        self.left_width = width - self.event_width

        # infobar
        self.info_font = pygame.font.Font(
            'freesansbold.ttf',
            fontsizes["info"]
        )
        self.infobar_height = height // 29
        self.info_pad = (self.infobar_height - fontsizes["info"]) // 2
        self.infobar_surface = pygame.Surface((self.left_width, self.infobar_height))
        renown_width = self.left_width // 4
        self.infobar_renown_rect = pygame.Rect(self.info_pad, self.info_pad, renown_width, self.infobar_height)
        self.infobar_cash_rect = pygame.Rect(
            (
                renown_width,                               # X
                self.info_pad,                              # Y
                self.left_width - (self.left_width // 4),   # Width
                self.infobar_height                         # Height
            )
        )

        # Stock area
        self.stock_height = (self.height - self.infobar_height) // 2
        self.stock_width = self.left_width

        self.stock_font = pygame.font.Font(
            'freesansbold.ttf',
            fontsizes['stock']
        )
        self.stock_title_font = pygame.font.Font(
            'freesansbold.ttf',
            fontsizes['title']
        )
        
        self.stock_surface = pygame.Surface((self.stock_width, self.stock_height))
        self.stock_title_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.left_width, self.infobar_height * 2
        )

        # Mask stock
        self.stock_mask_height = (self.height - self.stock_height) // 6
        self.stock_mask_width = self.left_width // 4
        self.stock_mask_surface = pygame.Surface((self.stock_mask_width, self.stock_mask_height))
        self.stock_mask_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )
        # Mask demand
        self.demand_mask_height = (self.height - self.stock_height) // 6
        self.demand_mask_width = self.left_width // 4
        self.demand_mask_surface = pygame.Surface((self.stock_mask_width, self.stock_mask_height))
        self.demand_mask_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )
        # antibac stock
        self.stock_antibac_height = (self.height - self.stock_height) // 6
        self.stock_antibac_width = self.left_width // 4
        self.stock_antibac_surface = pygame.Surface((self.stock_antibac_width, self.stock_antibac_height))
        self.stock_antibac_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )
        # antibac demand
        self.demand_antibac_height = (self.height - self.stock_height) // 6
        self.demand_antibac_width = self.left_width // 4
        self.demand_antibac_surface = pygame.Surface((self.stock_antibac_width, self.stock_antibac_height))
        self.demand_antibac_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )

        # visir stock
        self.stock_visir_height = (self.height - self.stock_height) // 6
        self.stock_visir_width = self.left_width // 4
        self.stock_visir_surface = pygame.Surface((self.stock_visir_width, self.stock_visir_height))
        self.stock_visir_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )
        # visir demand
        self.demand_visir_height = (self.height - self.stock_height) // 6
        self.demand_visir_width = self.left_width // 4
        self.demand_visir_surface = pygame.Surface((self.stock_visir_width, self.stock_visir_height))
        self.demand_visir_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )

        # ventilator stock
        self.stock_ventilator_height = (self.height - self.stock_height) // 6
        self.stock_ventilator_width = self.left_width // 4
        self.stock_ventilator_surface = pygame.Surface((self.stock_ventilator_width, self.stock_ventilator_height))
        self.stock_ventilator_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )
        # ventilator demand
        self.demand_ventilator_height = (self.height - self.stock_height) // 6
        self.demand_ventilator_width = self.left_width // 4
        self.demand_ventilator_surface = pygame.Surface((self.stock_ventilator_width, self.stock_ventilator_height))
        self.demand_ventilator_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )

        # glove stock
        self.stock_glove_height = (self.height - self.stock_height) // 6
        self.stock_glove_width = self.left_width // 4
        self.stock_glove_surface = pygame.Surface((self.stock_glove_width, self.stock_glove_height))
        self.stock_glove_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )
        # glove demand
        self.demand_glove_height = (self.height - self.stock_height) // 6
        self.demand_glove_width = self.left_width // 4
        self.demand_glove_surface = pygame.Surface((self.stock_glove_width, self.stock_glove_height))
        self.demand_glove_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )
        
        # toiler-paper stock
        self.stock_toilet_paper_height = (self.height - self.stock_height) // 6
        self.stock_toilet_paper_width = self.left_width // 4
        self.stock_toilet_paper_surface = pygame.Surface((self.stock_toilet_paper_width, self.stock_toilet_paper_height))
        self.stock_toilet_paper_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )
        # toiler-paper demand
        self.demand_toilet_paper_height = (self.height - self.stock_height) // 6
        self.demand_toilet_paper_width = self.left_width // 4
        self.demand_toilet_paper_surface = pygame.Surface((self.stock_toilet_paper_width, self.stock_toilet_paper_height))
        self.demand_toilet_paper_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )

        # production area
        self.production_cost = None
        self.production_rate = None
        self.production_height = (height - self.infobar_height) // 2
        self.production_ypos = self.production_height + self.infobar_height
        self.production_width = self.left_width //3 * 2
        self.production_surface = pygame.Surface((self.production_width, self.production_height))

        # Production title
        self.production_title_height = self.infobar_height
        self.production_title_rect = pygame.Rect(
           self.info_pad, self.info_pad, self.production_width, self.infobar_height
        )

        self.production_box_height = (self.production_height - self.production_title_height) // 3
        self.production_box_dimensions = (self.left_width // 3, self.production_box_height)
        
        self.mask_factory = FactoryBox(
            self.production_surface,
            self.production_box_dimensions, 
            "Mask Factories", 
            self.info_font, 
            pos=(0, 0)
        )
        
        self.glove_factory = FactoryBox(self.production_surface, self.production_box_dimensions, "Glove Factories", self.info_font, pos=(0, self.production_box_height))
        self.antibac_factory = FactoryBox(self.production_surface, self.production_box_dimensions, "Antibac Factories", self.info_font, pos=(0, self.production_box_height * 2))
        self.visir_factory = FactoryBox(self.production_surface, self.production_box_dimensions, "Visir Factories", self.info_font, pos=(self.left_width // 3, 0))
        self.ventilator_factory = FactoryBox(self.production_surface, self.production_box_dimensions, "Ventilator Factories", self.info_font, pos=(self.left_width // 3, self.production_box_height))
        self.toilet_paper_factory = FactoryBox(self.production_surface, self.production_box_dimensions, "Toilet paper Factories", self.info_font, pos=(self.left_width // 3, self.production_box_height * 2 ))

        for e in [
            self.mask_factory, self.glove_factory, self.antibac_factory, self.visir_factory, self.ventilator_factory, self.toilet_paper_factory
        ]:
            e.pos = (e.pos[0], e.pos[1]+self.production_title_height)

        # Off-the-books area
        self.offbooks_height = self.production_height
        self.offbooks_width = self.left_width-self.production_width
        self.offbooks_ypos = self.production_ypos
        self.offbooks_xpos = self.production_width
        self.offbooks_surface = pygame.Surface((self.offbooks_width, self.offbooks_height))

        # Off-the-boox title
        self.offbooks_title_height = self.infobar_height
        self.offbooks_title_rect = pygame.Rect(
           self.info_pad, self.info_pad, self.offbooks_width, self.offbooks_title_height
        )
        
        # off-the-books boxes
        self.offbooks_box_dimensions = (
            self.offbooks_width, (self.offbooks_height-self.offbooks_title_height) // 2
        )
        self.offbooks_moonshiners = OffBooksProducerBox(
            self.offbooks_surface, self.offbooks_box_dimensions,
            "Moonshiners producing cheap Antibac",
            self.info_font,
            pos=(0,self.offbooks_title_height)
        )
        self.offbooks_child_labor = OffBooksProducerBox(
            self.offbooks_surface, self.offbooks_box_dimensions,
            "Child labor mask production",
            self.info_font,
            pos=(0,self.offbooks_title_height+self.offbooks_box_dimensions[1])
        )

    def add_event(self, event):
        self.event_list.append(
            EventBox(
                self.event_surface,
                (self.event_width, self.event_height),
                event,
                self.event_font
            )
        )
    
    def pop_event(self):
        """Removes oldest event and blacks event area"""
        self.event_list = self.event_list[1:]
        self.event_surface.fill(colors.DARKER_GRAY)

    def update_gamedata(self, data):
        self.game_data = data

    def draw(self):

        # remove oldest event if old
        if self.event_list:
            if time.time() - self.event_list[0].created > 3:
                self.pop_event()

        self.event_surface.fill(colors.DARKER_GRAY)

        # Add event area at right edge of screen
        for i in range(len(self.event_list)):
            if i > 10: # max 10 events on screen
                break
            self.event_list[i].pos = (0, self.event_height*i)
            self.event_list[i].draw()
        self.screen.blit(self.event_surface, self.event_surface_pos)
      

        # info bar
        self.infobar_surface.fill(colors.DARK_GRAY)
        if not self.game_data:
            renown = "Renown: 50%"
            cash = "Cash: $1000"
        else:
            renown = f"Renown: {self.game_data['renown']}%"
            cash = f"Cash: ${self.game_data['cash']}"

        
        textwrap.draw_text(
            self.infobar_surface, 
            renown,
            colors.WHITE,
            self.infobar_renown_rect,
            self.info_font,
        )

        textwrap.draw_text(
            self.infobar_surface, 
            cash,
            colors.MONEY_GREEN,
            self.infobar_cash_rect,
            self.info_font,
        )

        self.screen.blit(self.infobar_surface, (0, 0))


        # Stock box
        self.stock_surface.fill(colors.DARKER_GRAY)
        stockTitle = "WAREHOUSE STOCK"
        textwrap.draw_text(
            self.stock_surface,
            stockTitle,
            colors.WHITE,
            self.stock_title_rect,
            self.stock_title_font,
        )

        # Mask stock
        self.stock_mask_surface.fill(colors.DARK_GRAY)
        stockMask = f"Masks: {self.game_data['mask stock']}"
        textwrap.draw_text(
            self.stock_mask_surface,
            stockMask,
            colors.WHITE,
            self.stock_mask_rect,
            self.stock_font
        )

        # Mask demand
        self.demand_mask_surface.fill(colors.DARK_GRAY)
        demandMask = f"Demand: {self.game_data['mask demand']}"    # Number of demand for
        if self.game_data['mask stock'] < self.game_data['mask demand']: # Check if stock is lower than demand
            demandColor = colors.DARK_RED
        else:
            demandColor = colors.MONEY_GREEN
        
        textwrap.draw_text(
            self.demand_mask_surface,
            demandMask,
            demandColor,
            self.demand_mask_rect,
            self.stock_font
        )
        
        # antibac stock
        self.stock_antibac_surface.fill(colors.DARK_GRAY)
        stockAntibac = f"Antibac: {self.game_data['antibac stock']}"
        textwrap.draw_text(
            self.stock_antibac_surface,
            stockAntibac,
            colors.WHITE,
            self.stock_antibac_rect,
            self.stock_font
        )

        # antibac demand
        self.demand_antibac_surface.fill(colors.DARK_GRAY)
        demandAntibac = f"Demand: {self.game_data['antibac demand']}"    # Number of demand for
        if self.game_data['antibac stock'] < self.game_data['antibac demand']: # Check if stock is lower than demand
            demandColor = colors.DARK_RED
        else:
            demandColor = colors.MONEY_GREEN
        
        textwrap.draw_text(
            self.demand_antibac_surface,
            demandAntibac,
            demandColor,
            self.demand_antibac_rect,
            self.stock_font
        )

        # visir stock
        self.stock_visir_surface.fill(colors.DARK_GRAY)
        stockVisir = f"Visir: {self.game_data['visir stock']}"
        textwrap.draw_text(
            self.stock_visir_surface,
            stockVisir,
            colors.WHITE,   
            self.stock_visir_rect,
            self.stock_font
        )

        # visir demand
        self.demand_visir_surface.fill(colors.DARK_GRAY)
        demandVisir = f"Demand: {self.game_data['visir demand']}"    # Number of demand for
        if self.game_data['visir stock'] < self.game_data['visir demand']: # Check if stock is lower than demand
            demandColor = colors.DARK_RED
        else:
            demandColor = colors.MONEY_GREEN
        
        textwrap.draw_text(
            self.demand_visir_surface,
            demandVisir,
            demandColor,
            self.demand_visir_rect,
            self.stock_font
        )

        # ventilator stock
        self.stock_ventilator_surface.fill(colors.DARK_GRAY)
        stockVentilator = f"Ventilator: {self.game_data['ventilator stock']}"
        textwrap.draw_text(
            self.stock_ventilator_surface,
            stockVentilator,
            colors.WHITE,   
            self.stock_ventilator_rect,
            self.stock_font
        )

        # ventilator demand
        self.demand_ventilator_surface.fill(colors.DARK_GRAY)
        demandVentilator = f"Demand: {self.game_data['ventilator demand']}"    # Number of demand for
        if self.game_data['ventilator stock'] < self.game_data['ventilator demand']: # Check if stock is lower than demand
            demandColor = colors.DARK_RED
        else:
            demandColor = colors.MONEY_GREEN
        
        textwrap.draw_text(
            self.demand_ventilator_surface,
            demandVentilator,
            demandColor,
            self.demand_ventilator_rect,
            self.stock_font
        )

        # glove stock
        self.stock_glove_surface.fill(colors.DARK_GRAY)
        stockGlove = f"Gloves: {self.game_data['glove stock']}"
        textwrap.draw_text(
            self.stock_glove_surface,
            stockGlove,
            colors.WHITE,   
            self.stock_glove_rect,
            self.stock_font
        )

        # glove demand
        self.demand_glove_surface.fill(colors.DARK_GRAY)
        demandGlove = f"Demand: {self.game_data['glove demand']}"    # Number of demand for
        if self.game_data['glove stock'] < self.game_data['glove demand']: # Check if stock is lower than demand
            demandColor = colors.DARK_RED
        else:
            demandColor = colors.MONEY_GREEN
        
        textwrap.draw_text(
            self.demand_glove_surface,
            demandGlove,
            demandColor,
            self.demand_glove_rect,
            self.stock_font
        )

        # toilet-paper stock
        self.stock_toilet_paper_surface.fill(colors.DARK_GRAY)
        stockTP = f"Toilet-paper: {self.game_data['toilet-paper stock']}"
        textwrap.draw_text(
            self.stock_toilet_paper_surface,
            stockTP,
            colors.WHITE,   
            self.stock_toilet_paper_rect,
            self.stock_font
        )

        # toilet-paper demand
        self.demand_toilet_paper_surface.fill(colors.DARK_GRAY)
        demandTP = f"Demand: {self.game_data['toilet-paper demand']}"    # Number of demand for
        if self.game_data['toilet-paper stock'] < self.game_data['toilet-paper demand']: # Check if stock is lower than demand
            demandColor = colors.DARK_RED
        else:
            demandColor = colors.MONEY_GREEN
        
        textwrap.draw_text(
            self.demand_toilet_paper_surface,
            demandTP,
            demandColor,
            self.demand_toilet_paper_rect,
            self.stock_font
        )

        self.screen.blit(self.stock_surface, (0, self.infobar_height)) # Warehouse
        # Left side, first column, row 1-3
        self.screen.blit(self.stock_mask_surface, (self.infobar_height, self.infobar_height * 2))   # Mask stock
        self.screen.blit(self.demand_mask_surface, (self.infobar_height, self.infobar_height * 4))  # Mask demand
        self.screen.blit(self.stock_antibac_surface, (self.infobar_height, self.infobar_height * 6))   # antibac stock
        self.screen.blit(self.demand_antibac_surface, (self.infobar_height, self.infobar_height * 8))  # antibac demand
        self.screen.blit(self.stock_visir_surface, (self.infobar_height, self.infobar_height * 10))   # visir stock
        self.screen.blit(self.demand_visir_surface, (self.infobar_height, self.infobar_height * 12))  # visir demand
        # Right side, second column, row 1-3
        self.screen.blit(self.stock_ventilator_surface, (self.left_width//2, self.infobar_height * 2))   # ventilator stock
        self.screen.blit(self.demand_ventilator_surface, (self.left_width//2, self.infobar_height * 4))  # ventilator demand
        self.screen.blit(self.stock_glove_surface, (self.left_width//2, self.infobar_height * 6))   # glove stock
        self.screen.blit(self.demand_glove_surface, (self.left_width//2, self.infobar_height * 8))  # glove demand
        self.screen.blit(self.stock_toilet_paper_surface, (self.left_width//2, self.infobar_height * 10))   # toilet-paper stock
        self.screen.blit(self.demand_toilet_paper_surface, (self.left_width//2, self.infobar_height * 12))  # toilet-paper demand

        
        
        # Production Area
        self.production_surface.fill(colors.PRODUCTION_BG)
        textwrap.draw_text(
            self.production_surface,
            "Factories (click to buy more)",
            colors.WHITE,
            self.production_title_rect,
            self.info_font,
        )


        # Mask
        self.mask_factory.production = self.game_data["mask factories"] * self.production_rate["mask factories"]
        self.mask_factory.cost = self.production_cost["mask factories"]
        self.mask_factory.draw()
        
        # Glove
        self.glove_factory.production = self.game_data["glove factories"] * self.production_rate["glove factories"]
        self.glove_factory.cost = self.production_cost["glove factories"]
        self.glove_factory.draw()
        
        # Antibac
        self.antibac_factory.production = self.game_data["antibac factories"] * self.production_rate["antibac factories"]
        self.antibac_factory.cost = self.production_cost["antibac factories"]
        self.antibac_factory.draw()

        # Visir
        self.visir_factory.production = self.game_data["visir factories"] * self.production_rate["visir factories"]
        self.visir_factory.cost = self.production_cost["visir factories"]
        self.visir_factory.draw()

        # Ventilator
        self.ventilator_factory.production = self.game_data["ventilator factories"] * self.production_rate["ventilator factories"]
        self.ventilator_factory.cost = self.production_cost["ventilator factories"]
        self.ventilator_factory.draw()

        # Toilet paper
        self.toilet_paper_factory.production = self.game_data["toilet-paper factories"] * self.production_rate["toilet-paper factories"]
        self.toilet_paper_factory.cost = self.production_cost["toilet-paper factories"]
        self.toilet_paper_factory.draw()

        # Blit
        self.screen.blit(self.production_surface, (0, self.production_ypos))


        # offbooks drawing
        self.offbooks_surface.fill(colors.OFFBOOKS_BG)
        textwrap.draw_text(
            self.offbooks_surface,
            "Off the books",
            colors.OFFBOOKS_TITLE,
            self.offbooks_title_rect,
            self.info_font,
        )
        self.offbooks_moonshiners.production = self.game_data["moonshiner factories"] * self.production_rate["moonshiner factories"]
        self.offbooks_moonshiners.cost = self.production_cost["moonshiner factories"]
        self.offbooks_moonshiners.draw()

        self.offbooks_child_labor.production = self.game_data["childlabor factories"] * self.production_rate["childlabor factories"]
        self.offbooks_child_labor.cost = self.production_cost["childlabor factories"]
        self.offbooks_child_labor.draw()

        self.screen.blit(self.offbooks_surface, (self.offbooks_xpos, self.offbooks_ypos))

    def update_production_data(self, cost, rate):
        self.production_cost = cost
        self.production_rate = rate
